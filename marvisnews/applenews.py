import requests

API_KEY = "ce9074ae831248739593899b788886b0"
URL = "https://newsapi.org/v2/everything"
ITEM = "Apple"

def fetch_news():
    params = {
        "q": f"{ITEM} prices OR {ITEM} market OR {ITEM} shortage OR {ITEM} supply", 
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY
    }
    
    response = requests.get(URL, params=params)
    data = response.json()

    if data.get("status") == "ok":
        articles = data.get("articles", [])
        if not articles:
            print(f"No relevant news found for {ITEM}.")
            return

        print(f"\n📰 Latest {ITEM} Market News:\n")
        for i, article in enumerate(articles[:5], start=1):
            print(f"{i}. {article['title']}")
            print(f"   Source: {article['source']['name']}")
            print(f"   URL: {article['url']}\n")
    else:
        print(f"Error fetching news: {data.get('message')}")

if __name__ == "__main__":
    fetch_news()