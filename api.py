from flask import Flask , request , jsonify
from news_summarization import fetch_news , comparative_analysis , text_to_speech

app = Flask(__name__)

@app.route('/get_news' , methods = ["GET"])

def get_news():
    company = request.args.get("company", "Tesla")  # Default to "Tesla" if no company name is provided
    news_data = fetch_news(company)
    summary_report = comparative_analysis(news_data)

    # Generate Hindi TTS using the translated Final Sentiment Analysis
    tts_file = text_to_speech(summary_report["Final Sentiment Analysis"])  # Translate and generate audio
    summary_report["Audio"] = tts_file  # Add the audio file path to the response

    return jsonify(summary_report)

if __name__ == '__main__':
    app.run(debug=True , host= '0.0.0.0' , port=5001)