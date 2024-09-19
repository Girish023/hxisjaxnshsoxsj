from flask import Flask, jsonify
from flask_cors import CORS
from flask import Blueprint, jsonify
import requests

# app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"])

# @app.route('/titles', methods=['GET'])

api_home_bp = Blueprint('home', __name__)
CORS(api_home_bp)

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

# @app.route('/recent_changes/<int:title_number>', methods=['GET'])
@api_home_bp.route('/recent_changes/<int:title_number>', methods=['GET'])
def get_recent_changes(title_number):
    url = f'https://www.ecfr.gov/api/versioner/v1/versions/title-{title_number}.json?issue_date%5Bgte%5D=2024-07-03'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'content_versions' in data and data['content_versions']:
            sections = data['content_versions']
            sorted_sections = sorted(sections, key=lambda x: x['amendment_date'], reverse=True)

            grouped_sections = {}
            for section in sorted_sections:
                date = section['amendment_date']
                if date not in grouped_sections:
                    grouped_sections[date] = []
                grouped_sections[date].append(section)

            recent_changes = []
            for date, sections in grouped_sections.items():
                sections_list = []
                for section in sections:
                    sections_list.append({
                        "part": section.get('part', '—'),
                        "subpart": section.get('subpart', '—'),
                        "identifier": section.get('identifier', '§ —'),
                        "name": section.get('name', '')
                    })
                recent_changes.append({
                    "date": date,
                    "sections": sections_list
                })
            return jsonify(recent_changes)
        else:
            return jsonify({"message": "No recent changes found for Title {}".format(title_number)})
    else:
        return jsonify({"error": "Failed to fetch data"}), 500
