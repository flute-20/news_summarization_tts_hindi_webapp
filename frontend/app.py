import streamlit as st 
import requests
from gtts import gTTS
from googletrans import Translator
from io import BytesIO

st.set_page_config(page_title="  News Sentiment Analyzer" , layout='wide')

st.title(" 📰 News Sentiment Analyzer with Hindi TTS" )

company_name = st.text_input("🏢 Enter Company Name")

if st.button("📡 Analyze News "):
    with st.spinner("⏳ Fetching news and analyzing sentiment...") :
        try:
            response = requests.get(f"https://news-summarization-tts-hindi-webapp.onrender.com/get_news?company={company_name}")
            response.raise_for_status()
            data = response.json()

            st.subheader("📌 Extracted Articles")
            for article in data["Articles"]:
                st.markdown(f"**📰 {article['Title']}**")
                st.write(f"🔍 *{article['Summary']}*")
                st.write(f"🟢 **Sentiment:** {article['Sentiment']}")
                st.write(f"📌 **Topics:** {', '.join(article['Topics'])}")
                st.markdown("---")
            
            # Display Comparative Sentiment Analysis
            
            st.subheader("📊 Comparative Sentiment Analysis")
            st.write("### Sentiment Distribution")
            st.json(data["Comparative Sentiment Score"]["Sentiment Distribution"])
            st.write("### Coverage Differences")
            for difference in data["Comparative Sentiment Score"]["Coverage Differences"]:
                st.write(f"- **Comparison:** {difference['Comparison']}")
                st.write(f"- **Impact:** {difference['Impact']}")
            st.write("### Topic Overlap")
            st.json(data["Comparative Sentiment Score"]["Topic Overlap"])

            # Display Final Sentiment Analysis
        
            st.markdown("### 📈 Final Sentiment Analysis")
            st.write(data["Final Sentiment Analysis"])
    
            # Translate to Hindi and generate TTS using gTTS
            st.subheader("🔊 Hindi Audio Summary")
            translator = Translator()
            hindi_text = translator.translate(data["Final Sentiment Analysis"], src='en', dest='hi').text
            st.write(f"**Hindi Translation**: {hindi_text}")
            
            # Generate audio with gTTS (without saving to file)
            tts = gTTS(text=hindi_text, lang='hi')
            audio_file = BytesIO()
            tts.write_to_fp(audio_file)
            audio_file.seek(0)

            # Play audio in Streamlit
            st.audio(audio_file, format="audio/mp3")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error fetching data from backend: {e}")
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
            