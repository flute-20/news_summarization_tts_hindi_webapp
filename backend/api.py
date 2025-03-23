#importing files required for backend 
from flask import Flask , request , jsonify
from news_summarization import fetch_news , comparative_analysis
from flask_cors import CORS
import os 
import json

app = Flask(__name__)
CORS(app) #enable cors for frontend

# defining route to get the input data 
@app.route('/get_news' , methods = ["GET"])

# function  getnews takes all the function from news_summarization.py and call to fetch the news articles
def get_news():
    # try and except block to handle the error
    try : 
        company = request.args.get("company", "Tesla")  # Default to "Tesla" if no company name is provided
        news_data = fetch_news(company)
        summary_report = comparative_analysis(news_data)
        return app.response_class(
            response=json.dumps(summary_report , sort_keys = False),
            status = 200 ,
            mimetype = 'application/json'
        )
    except Exception as e :
        return jsonify({"error" : str(e)}) , 500
    
#
if __name__ == '__main__':
    app.run(host='0.0.0.0' , port = int(os.getenv("PORT" , 5000)) , debug = False )
