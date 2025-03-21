import streamlit as st 
import requests

st.set_page_config(page_title="  News Sentiment Analyzer" , layout='wide')

st.title(" 📰 News Sentiment Analyzer with Hindi TTS" )

company_name = st.text_input("🏢 Enter Company Name")

if st.button("📡 Analyze News "):
    with st.spinner("⏳ Fetching news and analyzing sentiment...") :
        response = requests.get(f"http://127.0.0.1:5001/get_news?company={company_name}")

        if response.status_code == 200 :
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
    
            # Play Hindi Audio
            st.subheader("🔊 Hindi Audio Summary")
            st.audio(data["Audio"], format="audio/mp3")
        else:
            st.error("❌ Error fetching news. Please try again.")