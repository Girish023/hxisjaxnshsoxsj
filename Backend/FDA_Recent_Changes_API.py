from flask import Flask, Blueprint, jsonify, request
import requests
from flask_cors import CORS

api_recent_changes_bp = Blueprint('recent_changes', __name__)
CORS(api_recent_changes_bp, origins=["https://fda.ravooka.com"])

@api_recent_changes_bp.route('/recent_changes', methods=['GET'])
def get_recent_changes():
    url = 'https://www.ecfr.gov/api/versioner/v1/versions/title-21.json?issue_date%5Bgte%5D=2023-06-21'

    try:
        response = requests.get(url)
        response.raise_for_status()

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

            result = []
            for date, sections in grouped_sections.items():
                section_data = {
                    'date': date,
                    'count': len(sections),
                    'changes': []
                }
                for section in sections:
                    part = section.get('part', '—')
                    subpart = section.get('subpart', '—')
                    identifier = section.get('identifier', '§ —')
                    name = section.get('name', '')

                    section_data['changes'].append({
                        'part': part,
                        'subpart': subpart,
                        'identifier': identifier,
                        'name': name
                    })

                result.append(section_data)

            # Pagination logic
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
            start = (page - 1) * limit
            end = start + limit
            paginated_result = result[start:end]

            return jsonify({
                'data': paginated_result,
                'total': len(result),
                'page': page,
                'limit': limit
            })

        else:
            return jsonify({"message": "No recent changes found for Title 21."})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching data: {e}"}), 500
