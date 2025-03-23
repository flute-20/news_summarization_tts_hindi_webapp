Project Description:
This project is a cool web app that grabs the latest news about a company you choose! It pulls articles from big, non-JS news websites, extracts the top 10 unique news pieces with their title, summary, sentiment, and topics.
- Frontend: Built with Streamlit—super simple and user-friendly interface.
- Backend: Powered by Flask—handles all the heavy lifting like fetching and processing data.

Here’s what it does step-by-step:
1. Fetches 10 latest, non-repeating news articles for the company you enter.
2. Extracts key details: title, summary, sentiment (positive, negative, neutral), and topics.
3. Does a comparative analysis between the articles—checks how sentiments and topics differ.
4. Runs sentiment analysis and topic extraction to summarize the vibe of the news.
5. Finally, it figures out if the company’s news is mostly positive, negative, or neutral, and converts the summary into Hindi audio using text-to-speech!

Setup Instructions:
To get this app running on your machine, follow these steps:
1. Clone the Repository:
   git clone https://github.com/flute-20/news_summarization_tts_hindi_webapp.git
2. Install Dependencies:
   - Make sure you have Python installed (3.8 or higher works best).
   - Install all the libraries listed in requirements.txt:
     pip install -r requirements.txt
3. Modules and Libraries Used:
   - flask: Backend framework for APIs.
   - flask-cors: Handles cross-origin requests between frontend and backend.
   - streamlit: Builds the web interface.
   - beautifulsoup4: Scrapes news from websites.
   - gtts: Generates Hindi text-to-speech.
   - requests: Fetches web pages.
   - nltk: Helps with text processing and topic extraction.
   - textblob: Does sentiment analysis.
   - googletrans==4.0.0-rc1: Optional, for any translation needs.
4. Import Modules:
   - All these libraries should be imported in utils.py or news_summarization.py (whichever you’re using for utils).
5. Run the App:
   - Start the Flask backend:
     python api.py
   - Then launch the Streamlit frontend:
     streamlit run app.py

Usage:
1. Open the app in your browser (Streamlit usually runs at http://localhost:8501).
2. Type a company name (e.g., "Tesla") in the text box.
3. Hit the "Generate Report" button.
4. You’ll see a report with article titles, summaries, sentiments, and topics, plus a comparison of how the news varies.
5. At the end, it’ll play a Hindi audio summary of the overall sentiment!

API Development:
- No third-party APIs are used here.
- The Flask backend (api.py) handles internal APIs:
  - Fetches news data.
  - Processes it with sentiment and topic analysis.
  - Sends it to the Streamlit frontend.
- Test the APIs locally using tools like Postman by hitting endpoints like http://localhost:5001/get_news      (adjust based on your api.py setup).

Assumptions & Limitations:
- Assumptions:
  - News sites are scrape-friendly (non-JS, static HTML).
  - Internet connection is stable for fetching articles.
  - Hindi TTS works fine with gTTS—no heavy accents or custom voices.
- Limitations:
  - Can’t scrape JS-heavy sites (e.g., ones needing Selenium).
  - Limited to 10 articles—might miss some news if sites don’t have enough.
  - Sentiment analysis might not catch sarcasm or complex tones.

Deployment:
- Backend Deployed on render:
     - created flask and python files
     - pushed to this repo into backend directory
     - Then deployed the backend flask on render
     - used that link for connecting to front end
- Middle ware
     - As render automatically shutdowns the server
     - i have used uptimerobot
     - This will make the frontend to get a request
     - so that backend responds fastly even it gets shutdown
- Frontend Deployed on Hugging Face Spaces:
  - Link:   https://huggingface.co/spaces/vijayasris/news-sentiment-analyzer
- Steps to deploy:
  1. Push this repo to GitHub into Frontend directory
  2. Create a Space on Hugging Face, link your GitHub repo, and select Streamlit as the framework.
  3. Wait for the build—done!

Video Demo:
- Check out the demo here: [Insert YouTube/Google Drive link after recording].
- It’s a quick 2-3 minute walkthrough showing how to use the app and what it spits out!
