from flask import Flask, render_template, jsonify, request
import subprocess
import pymongo
from datetime import datetime
import socket
import json
from dotenv import load_dotenv
import os

load_dotenv()

mongoLink = os.getenv("MONGOLINK")

app = Flask(__name__)

# MongoDB setup
client = pymongo.MongoClient(f"{mongoLink}")
db = client["trending_data"]
collection = db["trends"]

# Route for the HTML page
@app.route('/')
def home():
    return render_template('./index.html')

# Route to run the Selenium script
@app.route('/run-script', methods=['GET'])
def run_script():
    try:
        # Run the Selenium script
        subprocess.run(["python", "./main.py"], check=True)
        
        # Fetch the latest record from MongoDB
        latest_record = collection.find_one(sort=[("date_time", -1)])
        
        # Extract data
        trends = latest_record.get("trends")
        ip_address = latest_record.get("ip_address")
        date_time = latest_record.get("date_time", "N/A")
        formatted_date = date_time.strftime("%d-%m-%Y")
        formatted_time = date_time.strftime("%H:%M")
        
        json_extract = latest_record
        
        # Render the HTML with updated data
        return render_template('./result.html', trends=trends, ip_address=ip_address, date=formatted_date, time=formatted_time, json_extract=json_extract)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
