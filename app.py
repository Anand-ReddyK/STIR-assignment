from flask import Flask, jsonify, render_template
from datetime import datetime
from final_scraper import TwitterScraper
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

app = Flask(__name__)

client = MongoClient(MONGO_URI)
db = client["twitter_data"]
collection = db["trending_topics"]

@app.route('/run-scraper', methods=['POST'])
def run_scraper_route():
    scraper = TwitterScraper()
    status = scraper.run()
    
    if status:
        result ={
            "status": "Scrapper Ran Successfully",
            "message": "Trending topics fetched and stored in MongoDB."
        }
    else:
        result = {
            "status": "Scrapper Failed",
            "message": "No trending topics fetched."
        }
    
    return jsonify(result)


@app.route('/', methods=['GET'])
def get_last_four_items():
    try:
        last_four = list(collection.find().sort("_id", -1).limit(4))

        last_four_clean = []
        for item in last_four:
            item_clean = {k: v for k, v in item.items() if k != "_id"}
            last_four_clean.append(item_clean)
        
        return render_template('index.html', last_four=last_four_clean)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
