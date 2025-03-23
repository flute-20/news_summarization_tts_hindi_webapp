# Import required libraries for web scraping, sentiment analysis, and NLP
from bs4 import BeautifulSoup
import requests
import sys
import nltk
from textblob import TextBlob
from collections import Counter, OrderedDict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure necessary NLTK resources are downloaded for tokenization and stopwords
nltk.download("punkt")
nltk.download("stopwords")

# Configure stdout to use UTF-8 encoding to handle special characters
sys.stdout.reconfigure(encoding="utf8")


def fetch_news(company_name):
    """
    Fetch news articles for a given company from BBC and extract relevant details.

    Args:
        company_name (str): Name of the company to search for.

    Returns:
        dict: Dictionary containing the company name and a list of articles with
              title, summary, sentiment, and topics.
    """
    # Construct the search URL for BBC news
    url = f"https://www.bbc.co.uk/search?q={company_name}&filter=news"

    # Send a GET request to the URL and parse the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Initialize an empty list to store articles
    articles = []

    # Extract up to 10 articles with their title, summary, sentiment, and topics
    for item in soup.find_all("div", class_="ssrcss-tq7xfh-PromoContent exn3ah913")[:10]:
        # Extract the title, default to "no title" if not found
        title = (
            item.find("p", class_="ssrcss-1b1mki6-PromoHeadline exn3ah910").text
            if item.find("p")
            else "no title"
        )

        # Extract the summary, default to empty string if not found
        summary = (
            item.find("p", class_="ssrcss-1q0x1qg-Paragraph e1jhz7w10").text
            if item.find("p")
            else ""
        )

        # Analyze the sentiment of the summary
        sentiment = analyze_sentiment(summary)

        # Extract key topics from the summary
        topics = extraction_topic(summary)

        # Append the article details as an OrderedDict to the articles list
        articles.append(
            OrderedDict(
                [
                    ("Title", title),
                    ("Summary", summary),
                    ("Sentiment", sentiment),
                    ("Topics", topics),
                ]
            )
        )

    # Return the company name and list of articles
    return {"Company": company_name, "Articles": articles}


def analyze_sentiment(text):
    """
    Analyze the sentiment of a given text using TextBlob.

    Args:
        text (str): Text to analyze for sentiment.

    Returns:
        str: Sentiment label ("Positive", "Negative", or "Neutral").
    """
    # Use TextBlob to analyze the sentiment of the text
    analysis = TextBlob(text)

    # Determine sentiment based on polarity score
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"


def extraction_topic(text, num_keywords=5):
    """
    Extract key topics (keywords) from a given text using NLTK.

    Args:
        text (str): Text to extract topics from.
        num_keywords (int): Number of keywords to extract (default: 5).

    Returns:
        list: List of up to `num_keywords` key topics (words).
    """
    # Tokenize the text into words and convert to lowercase
    words = word_tokenize(text.lower())

    # Get English stopwords to filter out common words
    stop_words = set(stopwords.words("english"))

    # Filter out stopwords and non-alphanumeric words, and extract keywords
    keywords = [word for word in words if word.isalnum() and word not in stop_words]

    # Return up to `num_keywords` keywords
    return list(keywords[:num_keywords])


def comparative_analysis(news_data):
    """
    Perform comparative sentiment analysis across news articles.

    Args:
        news_data (dict): Dictionary containing company name and list of articles.

    Returns:
        dict: Comparative analysis including sentiment distribution, coverage differences,
              topic overlap, final sentiment analysis, and audio placeholder.
    """
    # Extract articles from the news data
    articles = news_data["Articles"]

    # Get the sentiment of each article, default to "Neutral" if not found
    sentiments = [article.get("Sentiment", "Neutral") for article in articles]

    # Count the distribution of sentiments (Positive, Negative, Neutral)
    sentiment_count = Counter(sentiments)

    # Initialize a Counter to summarize topics across all articles
    topic_summary = Counter()

    # Collect topics from all articles
    for article in articles:
        for topic in article.get("Topics", []):
            # Ensure topic is a string (handle if topic is a tuple)
            if isinstance(topic, tuple):
                topic = topic[0]
            topic_summary[topic] += 1

    # Initialize list to store coverage differences
    coverage_differences = []

    # Get all unique topics
    unique_topics = list(topic_summary.keys())

    # Compare topics between consecutive articles to identify coverage differences
    if len(articles) > 1:
        for i in range(len(articles) - 1):
            comparison = (
                f"Article {i+1} focuses on {', '.join(articles[i]['Topics'])}, "
                f"whereas Article {i+2} discusses {', '.join(articles[i+1]['Topics'])}."
            )
            impact = "This shows how different perspectives exist within news coverage."
            coverage_differences.append({"Comparison": comparison, "Impact": impact})

    # Construct the final response with comparative analysis
    return {
        "Company": news_data["Company"],
        "Articles": articles,
        "Comparative Sentiment Score": {
            "Sentiment Distribution": dict(sentiment_count),
            "Coverage Differences": coverage_differences,
            "Topic Overlap": {
                "Common Topics": [
                    topic for topic, count in topic_summary.items() if count > 1
                ],
                "Unique Topics": unique_topics,
            },
        },
        "Final Sentiment Analysis": (
            f"{news_data['Company']}'s latest news coverage is mostly "
            f"{'Positive' if sentiment_count.get('Positive', 0) > sentiment_count.get('Negative', 0) else 'Negative'}."
        ),
        "Audio": "[Play Hindi Speech]",
    }
