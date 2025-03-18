import numpy as np
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
import csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from price_match import simple_items

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

for item in historical_data.keys():
    item_data = []
    dates = []

    for year in sorted(historical_data[item].keys()):
        for month in sorted(historical_data[item][year].keys()):
            if historical_data[item][year][month] is not None:
                try:
                    item_data.append(float(historical_data[item][year][month]))
                    dates.append(f"{year}-{month:02d}")
                except (ValueError, TypeError):
                    pass

    if item_data:
        plt.plot(range(len(item_data)), item_data, label=item, marker='o')


filtered_data = { k: v for k, v in historical_data.items()
    if deep_match_search(k) }
for item, value in filtered_data.items():
    print(item)

exit(0)

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
