# Import required libraries for the backend
from flask import Flask, request, jsonify
from news_summarization import fetch_news, comparative_analysis
from flask_cors import CORS
import os
import json

# Initialize Flask app
app = Flask(__name__)

# Enable CORS to allow cross-origin requests from the frontend
CORS(app)


# Define the API route to fetch news data
@app.route("/get_news", methods=["GET"])
def get_news():
    """
    API endpoint to fetch news articles for a given company and return a summary report.

    Args:
        company (str): Company name passed as a query parameter (default: "Tesla").

    Returns:
        JSON: Summary report with news articles and comparative analysis.
        Status 200 on success, 500 on error.
    """
    # Try-except block to handle potential errors during news fetching and processing
    try:
        # Get the company name from query parameters, default to "Tesla" if not provided
        company = request.args.get("company", "Tesla")

        # Fetch news articles for the given company using the fetch_news function
        news_data = fetch_news(company)

        # Generate a summary report with comparative analysis of the news articles
        summary_report = comparative_analysis(news_data)

        # Return the summary report as a JSON response with status 200
        return app.response_class(
            response=json.dumps(summary_report, sort_keys=False),
            status=200,
            mimetype="application/json",
        )

    # Handle any exceptions that occur during the process
    except Exception as e:
        # Return an error message with status 500
        return jsonify({"error": str(e)}), 500


# Run the Flask app if this script is executed directly
if __name__ == "__main__":
    # Run the app on host 0.0.0.0 and port (default 10000 if PORT env variable is not set)
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 10000)),
        debug=False,
    )
