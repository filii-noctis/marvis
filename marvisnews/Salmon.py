import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from transformers import GPT2LMHeadModel, GPT2Tokenizer

model_name = "gpt2"  
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Initialize Hugging Face NER pipeline and GPT-2 for reasoning generation
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

API_KEY = "ce9074ae831248739593899b788886b0"
NEWS_URL = "https://newsapi.org/v2/everything"
ITEM = "Salmon"

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
def scrape_article(url, num_paragraphs=3):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all paragraph tags within the article
        paragraphs = soup.find_all("p")

        # Take only the first `num_paragraphs` paragraphs
        article_text = " ".join([para.get_text() for para in paragraphs[:num_paragraphs]])

        return article_text, paragraphs  # Return both the truncated text and all paragraphs
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return "", []

# Function to count the number of keyword matches in an article
def count_keywords_in_article(article_text, keywords):
    text_lower = article_text.lower()
    return sum(text_lower.count(keyword) for keyword in keywords)

# Function to check if an article is relevant using keyword count and NER
def is_relevant(full_paragraphs, keywords):
    # Count keywords in the entire article
    article_text = " ".join([para.get_text() for para in full_paragraphs])
    keyword_count = count_keywords_in_article(article_text, keywords)

    return keyword_count

# Function to generate reasoning with GPT-2 about the article
def generate_reasoning(article_text):
    # Truncate the input text to ensure it's within the model's token limit
    max_input_length = 1024  # GPT-2 max token length
    
    # Tokenize and truncate
    tokens = tokenizer.encode(article_text, truncation=True, max_length=max_input_length)
    
    # Ensure that the number of tokens is within limits
    if len(tokens) > max_input_length:
        tokens = tokens[:max_input_length]

    # Decode back to text
    truncated_text = tokenizer.decode(tokens)
    
    # Add a prompt to request a general overview or summary
    prompt = f"Provide a brief analysis of the salmon market based on the following information:\n{truncated_text}"

    # Generate text with a smaller limit on new tokens (50 tokens) to avoid exceeding the token limit
    response = generator(prompt, max_new_tokens=50, truncation=True, num_return_sequences=1)
    
    # Extract the generated reasoning
    reasoning = response[0]['generated_text']
    return reasoning

# Main function to fetch, scrape, filter, and analyze articles
def main():
    articles = fetch_news()
    if not articles:
        return

    print(f"\n🔎 Filtering relevant {ITEM} price news...\n")

    # Define keywords for filtering
    keywords = ["price", "increase", "decrease", "market", "supply", "demand",
                "inflation", "cost", "trend", "shortage", "harvest", "economy", "drought"]
    
    # Score each article based on keyword occurrence
    article_scores = []
    for i, article in enumerate(articles, start=1):
        print(f"Scraping article {i} of {len(articles)}: {article['title']}")

        # Scrape full text and get both full paragraphs and the truncated text
        article_text, full_paragraphs = scrape_article(article["url"], num_paragraphs=3)

        # Skip empty articles
        if not article_text:
            continue

        # Count the number of keywords in the article
        keyword_count = is_relevant(full_paragraphs, keywords)
        article_scores.append((article, keyword_count))

    # Sort articles by keyword count in descending order and eliminate the two least relevant
    article_scores.sort(key=lambda x: x[1], reverse=True)
    relevant_articles = article_scores[:len(article_scores) - 2]  # Eliminate the bottom 2 articles

    print("\n🔎 Remaining relevant articles (after keyword filtering):")
    for i, (article, score) in enumerate(relevant_articles, start=1):
        print(f"Article {i}: {article['title']} - Keyword Count: {score}")

        # Scrape the relevant paragraphs for further reasoning generation
        article_text, full_paragraphs = scrape_article(article["url"], num_paragraphs=5)

        # Filter paragraphs that contain keywords related to pricing and economy
        relevant_paragraphs = [
            para.get_text() for para in full_paragraphs if any(keyword in para.get_text().lower() for keyword in keywords)
        ]

        # Limit the number of relevant paragraphs (e.g., only take the first 5)
        relevant_paragraphs = relevant_paragraphs[:5]

        # If we have relevant paragraphs, proceed with reasoning generation
        if relevant_paragraphs:
            relevant_text = " ".join(relevant_paragraphs)
            print(f"\n✅ RELEVANT: {article['title']}")
            print(f"   📌 Source: {article['source']['name']}")
            print(f"   🔗 URL: {article['url']}\n")

            # Generate reasoning using the filtered paragraphs
            reasoning = generate_reasoning(relevant_text)
            print(f"Reasoning for price change:\n{reasoning}\n")
        else:
            print(f"❌ NOT RELEVANT: {article['title']}\n")

if __name__ == "__main__":
    main()