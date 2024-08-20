from flask import Flask, jsonify
from flask_cors import CORS
from flask import Blueprint, jsonify
import requests

api_home_bp = Blueprint('home', __name__)
CORS(api_home_bp, origins=["https://vaisesika-fda.netlify.app"])

@api_home_bp.route('/titles', methods=['GET'])
def get_titles():
    url = 'https://www.ecfr.gov/api/versioner/v1/titles.json'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        titles_data = []
        for title in data["titles"]:
            titles_data.append({
                "number": title["number"],
                "name": title["name"],
                "latest_amended_on": title["latest_amended_on"]
            })
        return jsonify(titles_data)
    else:
        return jsonify({"error": "Failed to fetch data"}), 500


