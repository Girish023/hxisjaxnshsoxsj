# from flask import Flask, jsonify, request
# import requests
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"])

# @app.route('/api/recent_changes', methods=['GET'])
# def get_recent_changes():
#     url = 'https://www.ecfr.gov/api/versioner/v1/versions/title-21.json?issue_date%5Bgte%5D=2024-07-03'
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
        
#         if 'content_versions' in data and data['content_versions']:
#             sections = data['content_versions']
#             sorted_sections = sorted(sections, key=lambda x: x['amendment_date'], reverse=True)
#             grouped_sections = {}
#             for section in sorted_sections:
#                 date = section['amendment_date']
#                 if date not in grouped_sections:
#                     grouped_sections[date] = []
#                 grouped_sections[date].append(section)
#             return jsonify(grouped_sections)
#         else:
#             return jsonify({"message": "No recent changes found for Title 21."})
    
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/api/titles', methods=['GET'])
# def get_titles():
#     url = 'https://www.ecfr.gov/api/versioner/v1/titles.json'
#     params = {
#         'api_key': 'eW6Ilx8SndvThKyeuLBmCaUXOaUSW2Zt9vwe3iUn'
#     }
    
#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         data = response.json()
#         return jsonify(data)
    
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=8000)




from flask import Flask, jsonify
from flask_cors import CORS
from flask import Blueprint, jsonify
import requests

# app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"])

# @app.route('/titles', methods=['GET'])

api_home_bp = Blueprint('home', __name__)
CORS(api_home_bp, origins=["https://fda-vaisesika.netlify.app"])

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

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=8000)


