from bs4 import BeautifulSoup
import requests
import sys
import nltk
from textblob import TextBlob
from collections import Counter , OrderedDict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure necessary NLP resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')


sys.stdout.reconfigure(encoding = 'utf8')
def fetch_news(company_name):
    
    url = f'https://www.bbc.co.uk/search?q={company_name}&filter=news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text , 'html.parser')

    articles = []
    for item in soup.find_all('div' , class_ = 'ssrcss-tq7xfh-PromoContent exn3ah913')[ :10] :
        title = item.find('p', class_='ssrcss-1b1mki6-PromoHeadline exn3ah910').text if item.find('p') else "no title"
        summary = item.find('p' , class_ = 'ssrcss-1q0x1qg-Paragraph e1jhz7w10').text if item.find('p') else ''
        sentiment = analyze_sentiment(summary)
        topics = extraction_topic(summary)

        articles.append(OrderedDict([
            ('Title', title),
            ('Summary', summary),
            ('Sentiment', sentiment),
            ('Topics', topics)
        ]))
    return {"Company" : company_name , "Articles" : articles}

def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

def extraction_topic(text , num_keywords=5):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word.isalnum() and word not in stop_words]    
    return list(keywords[ : num_keywords])


def comparative_analysis(news_data):
    articles = news_data["Articles"]
    sentiments = [article.get("Sentiment", "Neutral") for article in articles]
    sentiment_count = Counter(sentiments)

    topic_summary = Counter()
    for article in articles:
        for topic in article.get("Topics" , []):
            if isinstance(topic, tuple):  # Ensure topic is a string
                topic = topic[0]
            topic_summary[topic] += 1 

        coverage_differences = []
        unique_topics = list(topic_summary.keys())
        
        if len(articles) > 1:
            for i in range(len(articles) - 1):
                comparison = f"Article {i+1} focuses on {', '.join(articles[i]['Topics'])}, whereas Article {i+2} discusses {', '.join(articles[i+1]['Topics'])}."
                impact = "This shows how different perspectives exist within news coverage."
                coverage_differences.append({"Comparison": comparison, "Impact": impact})
    
    return {
        "Company": news_data["Company"],
        "Articles": articles,
        "Comparative Sentiment Score": {
            "Sentiment Distribution": dict(sentiment_count),
            "Coverage Differences": coverage_differences,
            "Topic Overlap": {
                "Common Topics": [topic for topic, count in topic_summary.items() if count > 1],
                "Unique Topics": unique_topics
            }
        },
        "Final Sentiment Analysis": f"{news_data['Company']}'s latest news coverage is mostly {'Positive' if sentiment_count.get('Positive', 0) > sentiment_count.get('Negative', 0) else 'Negative'}.",
        "Audio": "[Play Hindi Speech]"
    }

