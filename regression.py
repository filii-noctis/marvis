import numpy as np
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
import csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from price_match import simple_items, items as matched_items, retailers, scrape_dispatcher

def deep_match_search(haystack: str) -> bool:
    haystack = haystack.lower()

    for needle in simple_items:
        if haystack.find(needle) != -1:
            return True

    return False


# stores parsed output from './historical_data.csv'
historical_data = {
    # "sample_product": {
    #     2017: [1.2, 5.6],
    #     2018: [1, 5, 6, 6, 3]
    # }
}

# load historical data from file
with open('historical_data.csv', mode='r') as file:
    csv_file = csv.reader(file)
    for line in csv_file:
        item: str = line.pop(0)
        if historical_data.get(item, None) is None:
            historical_data[item] = {}
        for month in range(len(line)):
            year_offset = month // 12
            local_month = month % 12 + 1
            if historical_data[item].get(2017 + year_offset, None) is None:
                historical_data[item][2017 + year_offset] = {}
            historical_data[item][2017 + year_offset][local_month] = line[month]

filtered_data = {}

current_year = 2025  # Assuming the current year is 2023
for k, v in historical_data.items():
    if deep_match_search(k):
        filtered_years = {year: months for year, months in v.items()
                         if year >= current_year - 5}
        if filtered_years:  # Only include item if it has data in the last 5 years
            filtered_data[k] = filtered_years

# Fetch current price data for each item from all retailers
for item in matched_items:
    item_key = None

    # Find the matching historical data key for this item
    for k in filtered_data.keys():
        if k.lower().find(item.lower()) != -1:
            item_key = k
            break

    if item_key is None:
        continue  # Skip if no matching historical data

    # Initialize the 2025 data if it doesn't exist
    if 2025 not in filtered_data[item_key]:
        filtered_data[item_key][2025] = {}

    # Get prices from all retailers and calculate average
    prices = []
    print(retailers)
    for retailer in retailers:
        price_str = scrape_dispatcher(retailer, item)
        print(f"scrape_dispatcher({retailer}, {item}) -> {price_str}")
        try:
            # Extract numeric price from string like '$5.99'
            if isinstance(price_str, str):
                price = float(price_str.replace('$', '').strip())
            else:
                price = float(price_str)
            prices.append(price)
            print(f"found price {price} for item {item}")
        except (ValueError, TypeError):
            continue  # Skip invalid prices

    # Calculate average price if we have any valid prices
    if prices:
        avg_price = sum(prices) / len(prices)
        print("march")
        filtered_data[item_key][2025][3] = str(round(avg_price, 2))  # Store as string for March (month 3)


dates = []
for item in filtered_data.keys():
    item_data = []
    item_dates = []

    for year in sorted(filtered_data[item].keys()):
        for month in sorted(filtered_data[item][year].keys()):
            if filtered_data[item][year][month] is not None:
                try:
                    item_data.append(float(filtered_data[item][year][month]))
                    item_dates.append(f"{year}-{month:02d}")
                except (ValueError, TypeError):
                    pass

    if item_data:
        plt.plot(range(len(item_data)), item_data, label=item, marker='o')
        if len(item_dates) > len(dates):
            dates = item_dates

for item, value in filtered_data.items():
    print(item)

plt.xlabel("Time Points")
plt.ylabel("Price/Value")
plt.title("Historical Data by Item")
plt.legend()
plt.xticks(range(len(dates)), dates, rotation=45)
plt.tight_layout()
plt.show()

exit(0)


# Load dataset, file that is currently being loaded is a placeholder so ignore that
df = pd.read_csv("price_data.csv")

# Assumes dataset already has a "date" column, uses that to convert into actual dates and calculate number of days
df['date'] = pd.to_datetime(df['date'])
df['total_days'] = (df['date'] - df['date'].min()).dt.days
x = df[['total_days']]
y = df['price']

# Set 20% to be tested, other 80% will be used for training
# Ensures that the data split is reproducible (42 is a common convention)
# Setting shuffle to false keeps the order of the data the same, important so that dates aren't mixed up in the process
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42, shuffle = False)

# Actual data, graphed from values in the CSV file
plt.figure(figsize=(10,5))
plt.plot(df['total_days'], df['price'], label = 'Actual Prices', marker = 'o')

# Define and train XGBoost model
xgb_model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, max_depth=3)
xgb_model.fit(x_train, y_train)

# Create price predictions
y_pred = xgb_model.predict(x_test)

# Evaluate Model
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"Model RMSE: {rmse:.2f}")

# Plot price predictions
plt.plot(x_test, y_test, label = 'Predicted prices', marker = 'x', linestyle = 'dashed')

plt.xlabel("Days Since Start")
plt.ylabel("Price")
plt.title("XGBoost Price Prediction")
plt.legend()
plt.show()


future_dates = np.arange(x['days_since_start'].max() + 1, x['days_since_start'].max() + 31).reshape(-1, 1)
future_prices = xgb_model.predict(future_dates)
future_df = pd.DataFrame({'days_since_start': future_dates.flatten(), 'predicted_price': future_prices})
print(future_df.head(10))  # Show first 10 predictions
