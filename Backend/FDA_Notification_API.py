from flask import Flask,Blueprint, jsonify
import requests
from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"])


# @app.route('/recent_changes', methods=['GET'])
api_notification_bp = Blueprint('notification', __name__)
CORS(api_notification_bp)

@api_notification_bp.route('/query', methods=['GET'])
def get_recent_changes():
    url = 'https://www.ecfr.gov/api/versioner/v1/versions/title-21.json?issue_date%5Bgte%5D=2024-08-16'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        data = response.json()

        if 'content_versions' in data and data['content_versions']:
            sections = data['content_versions']

            # Sort sections by amendment date (most recent first)
            sorted_sections = sorted(sections, key=lambda x: x['amendment_date'], reverse=True)

            grouped_sections = {}
            for section in sorted_sections:
                date = section['amendment_date']
                if date not in grouped_sections:
                    grouped_sections[date] = []
                grouped_sections[date].append(section)

            result = []
            for date, sections in grouped_sections.items():
                date_info = {
                    "date": date,
                    "sections_changed": len(sections),
                    "details": []
                }
                for section in sections:
                    part = section.get('part', '—')
                    subpart = section.get('subpart', '—')
                    identifier = section.get('identifier', '§ —')
                    name = section.get('name', '')

                    date_info["details"].append({
                        "part": part,
                        "subpart": subpart,
                        "identifier": identifier,
                        "name": name
                    })

                result.append(date_info)

            return jsonify(result)

        else:
            return jsonify({"message": "No recent changes found for Title 21."})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)})
