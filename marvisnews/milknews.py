import requests
from bs4 import BeautifulSoup
import spacy

# Load SpaCy's English NLP model
nlp = spacy.load("en_core_web_sm")

API_KEY = "ce9074ae831248739593899b788886b0"
NEWS_URL = "https://newsapi.org/v2/everything"
ITEM = "Milk"

# Function to fetch latest news articles
def fetch_news():
    params = {
        "q": f"{ITEM} prices OR {ITEM} market OR {ITEM} shortage OR {ITEM} supply",
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY
    }
    
    response = requests.get(NEWS_URL, params=params)
    data = response.json()

    if data.get("status") == "ok":
        articles = data.get("articles", [])
        if not articles:
            print(f"No relevant news found for {ITEM}.")
            return []
        
        return articles[:5]  # Return the first 5 articles
    else:
        print(f"Error fetching news: {data.get('message')}")
        return []

# Function to scrape article content
def scrape_article(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all paragraph tags within the article
        paragraphs = soup.find_all("p")

        # Join all paragraphs to get full article text
        article_text = " ".join([para.get_text() for para in paragraphs])

        return article_text
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return ""

# Function to check if an article is relevant
def is_relevant(article_text):
    keywords = ["price", "increase", "decrease", "market", "supply", "demand",
                "inflation", "cost", "trend", "shortage", "harvest", "economy", "drought"]

    text_lower = article_text.lower()
    
    # If at least one keyword is found, continue checking deeper with NLP
    if not any(word in text_lower for word in keywords):
        return False
    
    # Process article text with SpaCy
    doc = nlp(article_text)
    prices = [ent.text for ent in doc.ents if ent.label_ == "MONEY"]
    economic_factors = [sent.text for sent in doc.sents if "due to" in sent.text or "because of" in sent.text]

    return bool(prices) or bool(economic_factors)

# Main function to fetch, scrape, and filter articles
def main():
    articles = fetch_news()
    if not articles:
        return

    print(f"\n🔎 Filtering relevant {ITEM} price news...\n")
    
    for i, article in enumerate(articles, start=1):
        print(f"Scraping article {i} of {len(articles)}: {article['title']}")

        # Scrape full text
        article_text = scrape_article(article["url"])

        # Skip empty articles
        if not article_text:
            continue

        # Check if article is relevant
        if is_relevant(article_text):
            print(f"\n✅ RELEVANT: {article['title']}")
            print(f"   📌 Source: {article['source']['name']}")
            print(f"   🔗 URL: {article['url']}\n")
        else:
            print(f"❌ NOT RELEVANT: {article['title']}\n")

if __name__ == "__main__":
    main()