# Import required libraries for the frontend
import streamlit as st
import requests
from gtts import gTTS
from deep_translator import GoogleTranslator
from io import BytesIO


def main():
    """
    Main function to run the Streamlit app for news sentiment analysis and Hindi TTS.
    """
    # Set page configuration for better layout and title
    st.set_page_config(page_title="News Sentiment Analyzer", layout="wide")

    # Display the app title with an emoji
    st.title("📰 News Sentiment Analyzer with Hindi TTS")

    # Input field for company name with an emoji
    company_name = st.text_input("🏢 Enter Company Name")

    # Button to trigger news analysis with an emoji
    if st.button("📡 Analyze News"):
        # Show a spinner while fetching and processing data
        with st.spinner("⏳ Fetching news and analyzing sentiment..."):
            # Try-except block to handle potential errors during API calls and processing
            try:
                # Make a GET request to the backend API to fetch news data
                response = requests.get(
                    f"https://news-summarization-tts-hindi-webapp.onrender.com/get_news?company={company_name}"
                )
                response.raise_for_status()  # Raise an error for bad status codes
                data = response.json()  # Parse the JSON response

                # Store the fetched data in session state to persist across reruns
                st.session_state["data"] = data
                st.session_state["company_name"] = company_name

            # Handle API request errors
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error fetching data from backend: {e}")
                st.session_state["data"] = None  # Reset data on error

            # Handle other unexpected errors
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
                st.session_state["data"] = None  # Reset data on error

    # Check if data exists in session state (i.e., news has been fetched)
    if "data" in st.session_state and st.session_state["data"] is not None:
        data = st.session_state["data"]  # Retrieve data from session state

        # Display the company name as a header
        st.header(f"News Analysis for {data['Company']}")

        # Extract all unique topics for the dropdown
        all_topics = set()
        for article in data["Articles"]:
            all_topics.update(article["Topics"])
        all_topics = sorted(list(all_topics))

        # Add a dropdown to filter articles by topic
        st.subheader("Filter Articles by Topic")
        selected_topic = st.selectbox(
            "Select a topic to filter articles (or 'All' to show all):",
            ["All"] + all_topics,
        )

        # Filter articles based on the selected topic
        if selected_topic == "All":
            filtered_articles = data["Articles"]
        else:
            filtered_articles = [
                article
                for article in data["Articles"]
                if selected_topic in article["Topics"]
            ]

        # Display filtered articles
        st.subheader("📌 Extracted Articles")
        if filtered_articles:
            for article in filtered_articles:
                st.markdown(f"**📰 {article['Title']}**")  # Article title
                st.write(f"🔍 *{article['Summary']}*")  # Article summary
                st.write(f"🟢 **Sentiment:** {article['Sentiment']}")  # Sentiment
                st.write(f"📌 **Topics:** {', '.join(article['Topics'])}")  # Topics
                st.markdown("---")  # Separator between articles
        else:
            st.write("No articles found for the selected topic.")

        # Display comparative sentiment analysis
        st.subheader("📊 Comparative Sentiment Analysis")

        # Display sentiment distribution
        st.write("### Sentiment Distribution")
        st.json(data["Comparative Sentiment Score"]["Sentiment Distribution"])

        # Display coverage differences between articles
        st.write("### Coverage Differences")
        for difference in data["Comparative Sentiment Score"]["Coverage Differences"]:
            st.write(f"- **Comparison:** {difference['Comparison']}")
            st.write(f"- **Impact:** {difference['Impact']}")

        # Display topic overlap across articles
        st.write("### Topic Overlap")
        st.json(data["Comparative Sentiment Score"]["Topic Overlap"])

        # Display the final sentiment analysis
        st.markdown("### 📈 Final Sentiment Analysis")
        st.write(data["Final Sentiment Analysis"])

        # Translate the final sentiment analysis to Hindi and generate TTS
        st.subheader("🔊 Hindi Audio Summary")
        translator = GoogleTranslator(source="en", target="hi")  # Initialize translator
        hindi_text = translator.translate(data["Final Sentiment Analysis"])  # Translate to Hindi
        st.write(f"**Hindi Translation**: {hindi_text}")  # Display the translated text

        # Generate audio with gTTS (without saving to file)
        tts = gTTS(text=hindi_text, lang="hi")  # Create TTS object for Hindi
        audio_file = BytesIO()  # Create an in-memory file for audio
        tts.write_to_fp(audio_file)  # Write audio to the in-memory file
        audio_file.seek(0)  # Reset file pointer to the beginning

        # Play the audio in Streamlit
        st.audio(audio_file, format="audio/mp3")


# Run the app if this script is executed directly
if __name__ == "__main__":
    main()
