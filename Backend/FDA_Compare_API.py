# from flask import Flask, request, Blueprint, jsonify
# import xml.etree.ElementTree as ET
# import requests
# import re
# from flask_cors import CORS
# from datetime import datetime

# api_compare_bp = Blueprint('compare', __name__)
# # CORS(api_compare_bp, origins=["https://vaisesika-fda.netlify.app"])
# CORS(api_compare_bp, origins=["https://fda.ravooka.com"])
# # GitHub configuration
# GITHUB_REPO_OWNER = 'Girish023'
# GITHUB_REPO_NAME = 'FDA_Title-21'
# GITHUB_BRANCH_NAME = 'main'  # or the branch you are using

# def get_raw_url(owner, repo, branch, path):
#     """Construct the raw URL for a file in a GitHub repo."""
#     return f'https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}'

# def load_xml(date):
#     file_name = 'title-21.xml'
#     xml_path = f'versions/{date}/{file_name}'
#     raw_url = get_raw_url(GITHUB_REPO_OWNER, GITHUB_REPO_NAME, GITHUB_BRANCH_NAME, xml_path)

#     try:
#         # Download the XML content from GitHub
#         response = requests.get(raw_url)
#         response.raise_for_status()
#         xml_content = response.text
#         print(f"Downloaded XML content from GitHub: {raw_url}")

#         # Parse the XML content
#         root = ET.fromstring(xml_content)
#         print(f"Parsed XML content successfully from GitHub")
#         return root

#     except requests.RequestException as e:
#         print(f"Error downloading XML file from GitHub: {e}")
#         return None
#     except ET.ParseError as e:
#         print(f"Failed to parse XML content from GitHub: {e}")
#         return None
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         return None

# def normalize_title(title):
#     """Normalize the title for consistent comparison."""
#     return re.sub(r'\s+', ' ', title.strip()).lower()

# def get_all_titles_parts_and_sections(root):
#     if root is None:
#         return []

#     items = []
#     for chapter in root.findall(".//DIV3[@TYPE='CHAPTER']"):
#         chapter_title = chapter.find("HEAD").text.strip() if chapter.find("HEAD") is not None else "Unknown"
#         items.append({"title": normalize_title(chapter_title), "element": chapter})

#         if chapter.get("N") == "I":
#             for subchapter in chapter.findall(".//DIV4[@TYPE='SUBCHAP']"):
#                 subchapter_title = subchapter.find("HEAD").text.strip() if subchapter.find("HEAD") is not None else "Unknown"
#                 items.append({"title": normalize_title(subchapter_title), "element": subchapter})
#                 for part in subchapter.findall(".//DIV5[@TYPE='PART']"):
#                     part_title = part.find("HEAD").text.strip() if part.find("HEAD") is not None else "Unknown"
#                     items.append({"title": normalize_title(part_title), "element": part})
#                     for subpart in part.findall(".//DIV6[@TYPE='SUBPART']"):
#                         subpart_title = subpart.find("HEAD").text.strip() if subpart.find("HEAD") is not None else "Unknown"
#                         items.append({"title": normalize_title(subpart_title), "element": subpart})
#                         for section in subpart.findall(".//DIV8[@TYPE='SECTION']"):
#                             section_title = section.find("HEAD").text.strip() if section.find("HEAD") is not None else "Unknown"
#                             items.append({"title": normalize_title(section_title), "element": section})
#         else:
#             for part in chapter.findall(".//DIV5[@TYPE='PART']"):
#                 part_title = part.find("HEAD").text.strip() if part.find("HEAD") is not None else "Unknown"
#                 items.append({"title": normalize_title(part_title), "element": part})
#                 for section in part.findall(".//DIV6[@TYPE='SECTION']"):
#                     section_title = section.find("HEAD").text.strip() if section.find("HEAD") is not None else "Unknown"
#                     items.append({"title": normalize_title(section_title), "element": section})
#     return items

# # def search_query(query, items):
# #     normalized_query = normalize_title(query)
# #     matches = [item for item in items if normalized_query in item["title"]]
# #     print(f"Searching for '{query}', found matches: {[match['title'] for match in matches]}")
# #     return matches

# def search_query(query, items):
#     # Normalize the query for consistent comparison
#     normalized_query = normalize_title(query)
    
#     # List to store potential matches
#     matches = []

    
    
#     numeric_match = re.search(r'\d+(\.\d+)?', query)  # Match numbers like "112.3"
#     symbol_match = re.search(r'§\s*\d+(\.\d+)?', query) 
#     number_pattern = r'§?\s*\d+(\.\d+)?'
#     exact_match_query = re.findall(number_pattern, query)

#     if numeric_match or symbol_match:
#         # If there's a numeric or symbol-based query, prioritize exact matches
#         matches = [item for item in items if numeric_match.group() in item["title"] ]#or symbol_match.group() in item["title"]]
#     else:
#         # Fall back to normal text-based search
#         matches = [item for item in items if normalized_query in item["title"]]
    
#     if exact_match_query:
#         exact_match = exact_match_query[0].strip()
#         # Exact matches should prioritize title match with the exact text
#         matches = [item for item in items if exact_match in item["title"]]

#     # If no exact match is found, proceed with a flexible phrase match
#     if not matches:
#         matches = [item for item in items if normalized_query in item["title"]]

#     # If still no matches, try broader or partial matching
#     if not matches:
#         # Split the normalized query into words and try partial matches
#         query_words = normalized_query.split()
#         matches = [item for item in items if all(word in item["title"] for word in query_words)]

#     # Prioritize matches by the length of matched phrases (closer to the full query)
#     matches.sort(key=lambda item: len(set(normalized_query.split()) & set(item["title"].split())), reverse=True)

#     #print(f"Searching for '{query}', found matches: {[match['title'] for match in matches]}")
#     return matches



# def display_selected_element(element, max_lines=20):
#     content = ""
#     for child in element.iter():
#         if child.tag in ["HEAD", "P", "p", "I"]:
#             text = ""
#             if child.text:
#                 text += child.text.strip()
#             if child.tail:
#                 text += child.tail.strip()

#             if child.tag == "I":
#                 content += f"*{text}*\n"
#             elif child.tag in ["P", "p"]:
#                 content += f"{text}\n"
#             else:
#                 content += f"{text}\n"

#     lines = content.split("\n")
#     if len(lines) > max_lines:
#         content = "\n".join(lines[:max_lines]) + "\n...\n"

#     return content

# # def extract_main_terminology(query):
# #     query = query.lower().strip()
# #     phrases_to_remove = [
# #         "what is", "tell me about", "explain about", "explain me about", "explain"
# #     ]
# #     pattern = r'\b(?:' + '|'.join(map(re.escape, phrases_to_remove)) + r')\b'
# #     cleaned_query = re.sub(pattern, '', query).strip()
# #     cleaned_query = re.sub(r'[^\w\s]', '', cleaned_query)
# #     stop_words = set([
# #         "the", "is", "in", "at", "of", "on", "and", "a", "an", "to", "for", "about", "with", "me", "about", "is", "are", "am"
# #     ])
# #     keywords = [word for word in cleaned_query.split() if word not in stop_words]
# #     main_query = ' '.join(keywords)
# #     return main_query.strip()

# def extract_main_terminology(query):
#     query = query.lower().strip()
#     phrases_to_remove = [
#         "what is", "tell me about", "explain about", "explain me about", "explain"
#     ]
#     pattern = r'\b(?:' + '|'.join(map(re.escape, phrases_to_remove)) + r')\b'
#     cleaned_query = re.sub(pattern, '', query).strip()

#     # Preserve numeric and symbolic content
#     cleaned_query = re.sub(r'[^\w\s§\d.]', '', cleaned_query)

#     stop_words = set([
#         "the", "is", "in", "at", "of", "on", "and", "a", "an", "to", "for", "about", "with", "me", "about", "is", "are", "am"
#     ])
#     keywords = [word for word in cleaned_query.split() if word not in stop_words]
#     main_query = ' '.join(keywords)
#     return main_query.strip()


# def get_latest_date():
#     try:
#         # Fetch the list of files from the 'versions' directory in the GitHub repository
#         response = requests.get(f'https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/versions?ref={GITHUB_BRANCH_NAME}')
#         response.raise_for_status()
#         files = response.json()

#         # Extract dates from file paths
#         dates = set()
#         for file in files:
#             if file['type'] == 'dir':
#                 date_str = file['name']
#                 try:
#                     # Validate date format
#                     datetime.strptime(date_str, '%Y-%m-%d')
#                     dates.add(date_str)
#                 except ValueError:
#                     continue

#         if not dates:
#             return None

#         # Get the latest date
#         latest_date = max(dates, key=lambda d: datetime.strptime(d, '%Y-%m-%d'))
#         return latest_date

#     except requests.RequestException as e:
#         print(f"Error fetching dates from GitHub: {e}")
#         return None

# @api_compare_bp.route('/query', methods=['POST'])
# def handle_request():
#     data = request.get_json()
#     query = data.get('query')
#     selected_option = data.get('selected_option')
#     compare_date = data.get('date')

#     if not query:
#         return jsonify({"error": "Query not provided"}), 400

#     main_query = extract_main_terminology(query)

#     # Handle query part
#     current_date = get_latest_date()  # Get the latest date from GitHub
#     if not current_date:
#         return jsonify({"error": "Failed to determine the current date"}), 500

#     root = load_xml(current_date)
#     if root is None:
#         return jsonify({"error": "Failed to load XML content"}), 500

#     all_items = get_all_titles_parts_and_sections(root)
#     matches = search_query(main_query, all_items)

#     if len(matches) == 0:
#         response = {"result": "No matches found."}
#     elif len(matches) == 1 or selected_option:
#         if selected_option:
#             normalized_selected_option = normalize_title(selected_option)
#             selected_element = next((item["element"] for item in matches if item["title"] == normalized_selected_option), None)
#         else:
#             selected_element = matches[0]["element"]

#         if selected_element:
#             selected_content = display_selected_element(selected_element)
#             response = {"result": selected_content, "current_date": current_date}
#         else:
#             response = {"error": "Selected option not found"}
#             return jsonify(response), 400
#     else:
#         options = [match["title"] for match in matches]
#         response = {"result": "Multiple matches found. Choose one.", "options": options}
    
#     # Handle compare part
#     if compare_date:
#         if not compare_date:
#             return jsonify({"error": "Comparison date not provided"}), 400

#         compare_root = load_xml(compare_date)
#         if compare_root is None:
#             return jsonify({"error": f"Failed to load XML content for comparison date {compare_date}"}), 500

#         compare_items = get_all_titles_parts_and_sections(compare_root)
#         compare_normalized_option = normalize_title(selected_option)
#         compare_element = next((item["element"] for item in compare_items if item["title"] == compare_normalized_option), None)

#         if not compare_element:
#             return jsonify({"error": f"Selected option not found in comparison date {compare_date}"}), 400

#         compare_content = display_selected_element(compare_element)
#         response["comparison"] = compare_content

#     return jsonify(response)

# @api_compare_bp.route('/available_dates', methods=['GET'])
# def get_available_dates():
#     try:
#         response = requests.get(f'https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/versions?ref={GITHUB_BRANCH_NAME}')
#         response.raise_for_status()
#         files = response.json()

#         dates = []
#         for file in files:
#             if file['type'] == 'dir':
#                 date_str = file['name']
#                 try:
#                     # Validate date format
#                     datetime.strptime(date_str, '%Y-%m-%d')
#                     dates.append(date_str)
#                 except ValueError:
#                     continue

#         return jsonify({"dates": sorted(dates, reverse=True)})
    
#     except requests.RequestException as e:
#         return jsonify({"error": f"Error fetching dates from GitHub: {e}"}), 500

# # if __name__ == '__main__':
# #     app.run(port=8000, debug=True)




#BLOB CODE
from flask import Flask, Blueprint, request, jsonify
import xml.etree.ElementTree as ET
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError
import re
import os
import io
from flask_cors import CORS
from datetime import datetime

api_compare_bp = Blueprint('compare', __name__)
CORS(api_compare_bp)

# Azure Blob Storage configuration
connect_str = "DefaultEndpointsProtocol=https;AccountName=girishstorage;AccountKey=NFELbghvGk/kNC2gZ7YW5IbD2/3rygek0isMs4XvhRdM9LIqSMo+MwNaNYfCO0Aoax9vhvDaAfLZ+AStPgBq9w==;EndpointSuffix=core.windows.net"
container_name = "versions"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)

def load_xml(date):
    file_name = 'title-21.xml'
    blob_path = f'{date}/{file_name}'

    def fetch_blob():
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)
        try:
            xml_content = blob_client.download_blob().content_as_text()
            return xml_content
        except AzureError as e:
            print(f"Error downloading XML file from Azure Blob Storage: {e}")
            return None

    xml_content = fetch_blob()
    if xml_content is None:
        return None

    try:
        root = ET.fromstring(xml_content)
        return root
    except ET.ParseError as e:
        print(f"Failed to parse XML content: {e}")
        return None

def normalize_title(title):
    """Normalize the title for consistent comparison."""
    return re.sub(r'\s+', ' ', title.strip()).lower()


def get_all_titles_parts_and_sections(root):
    if root is None:
        return []

    items = []
    for chapter in root.findall(".//DIV3[@TYPE='CHAPTER']"):
        chapter_title = chapter.find("HEAD").text.strip() if chapter.find("HEAD") is not None else "Unknown"
        items.append({"title": normalize_title(chapter_title), "element": chapter})

        if chapter.get("N") == "I":
            for subchapter in chapter.findall(".//DIV4[@TYPE='SUBCHAP']"):
                subchapter_title = subchapter.find("HEAD").text.strip() if subchapter.find("HEAD") is not None else "Unknown"
                items.append({"title": normalize_title(subchapter_title), "element": subchapter})
                for part in subchapter.findall(".//DIV5[@TYPE='PART']"):
                    part_title = part.find("HEAD").text.strip() if part.find("HEAD") is not None else "Unknown"
                    items.append({"title": normalize_title(part_title), "element": part})
                    for subpart in part.findall(".//DIV6[@TYPE='SUBPART']"):
                        subpart_title = subpart.find("HEAD").text.strip() if subpart.find("HEAD") is not None else "Unknown"
                        items.append({"title": normalize_title(subpart_title), "element": subpart})
                        for section in subpart.findall(".//DIV8[@TYPE='SECTION']"):
                            section_title = section.find("HEAD").text.strip() if section.find("HEAD") is not None else "Unknown"
                            items.append({"title": normalize_title(section_title), "element": section})
        else:
            for part in chapter.findall(".//DIV5[@TYPE='PART']"):
                part_title = part.find("HEAD").text.strip() if part.find("HEAD") is not None else "Unknown"
                items.append({"title": normalize_title(part_title), "element": part})
                for section in part.findall(".//DIV6[@TYPE='SECTION']"):
                    section_title = section.find("HEAD").text.strip() if section.find("HEAD") is not None else "Unknown"
                    items.append({"title": normalize_title(section_title), "element": section})
    return items

def search_query(query, items):
    normalized_query = normalize_title(query)
    matches = []

    # Extract numeric part from the query
    numeric_match = re.search(r'\d+(\.\d+)?', query)
    if numeric_match:
        numeric_query = numeric_match.group()
        numeric_query_value = float(numeric_query) if '.' in numeric_query else int(numeric_query)

    # Define a function to extract numeric part from title
    def extract_numeric_from_title(title):
        match = re.search(r'\d+(\.\d+)?', title)
        return float(match.group()) if match else None

    # Search logic
    for item in items:
        title = item["title"]
        numeric_title = extract_numeric_from_title(title)
        
        # Check if the numeric part of the title matches the query
        if numeric_match and numeric_title is not None:
            if numeric_title == numeric_query_value:
                matches.append(item)
        elif normalized_query in title:
            matches.append(item)

    # Sort matches by the relevance of the numeric value
    matches.sort(key=lambda item: (
        extract_numeric_from_title(item["title"]) if extract_numeric_from_title(item["title"]) is not None else float('inf'),
        len(set(normalized_query.split()) & set(item["title"].split()))
    ), reverse=True)

    return matches



def display_selected_element(element, max_lines=20):
    content = ""
    for child in element.iter():
        if child.tag in ["HEAD", "P", "p", "I"]:
            text = ""
            if child.text:
                text += child.text.strip()
            if child.tail:
                text += child.tail.strip()

            if child.tag == "I":
                content += f"*{text}*\n"
            elif child.tag in ["P", "p"]:
                content += f"{text}\n"
            else:
                content += f"{text}\n"

    lines = content.split("\n")
    if len(lines) > max_lines:
        content = "\n".join(lines[:max_lines]) + "\n...\n"

    return content



def extract_main_terminology(query):
    query = query.lower().strip()
    phrases_to_remove = [
        "what is", "tell me about", "explain about", "explain me about", "explain"
    ]
    pattern = r'\b(?:' + '|'.join(map(re.escape, phrases_to_remove)) + r')\b'
    cleaned_query = re.sub(pattern, '', query).strip()

    cleaned_query = re.sub(r'[^\w\s§\d.]', '', cleaned_query)

    stop_words = set([
        "the", "is", "in", "at", "of", "on", "and", "a", "an", "to", "for", "about", "with", "me", "about", "is", "are", "am"
    ])
    keywords = [word for word in cleaned_query.split() if word not in stop_words]
    main_query = ' '.join(keywords)
    return main_query.strip()

def get_latest_date():
    try:
        blobs = blob_service_client.get_container_client(container_name).list_blobs()
        dates = set()
        for blob in blobs:
            parts = blob.name.split('/')
            if len(parts) > 1:
                date_str = parts[0]
                try:
                    datetime.strptime(date_str, '%Y-%m-%d')
                    dates.add(date_str)
                except ValueError:
                    continue

        if not dates:
            return None

        latest_date = max(dates, key=lambda d: datetime.strptime(d, '%Y-%m-%d'))
        return latest_date

    except AzureError as e:
        print(f"Error listing blobs from Azure Blob Storage: {e}")
        return None

@api_compare_bp.route('/query', methods=['POST'])
def handle_request():
    data = request.get_json()
    query = data.get('query')
    compare_date = data.get('date')

    if not query:
        return jsonify({"error": "Query not provided"}), 400

    main_query = extract_main_terminology(query)

    # Handle query part
    current_date = get_latest_date()
    if not current_date:
        return jsonify({"error": "Failed to determine the current date"}), 500

    root = load_xml(current_date)
    if root is None:
        return jsonify({"error": "Failed to load XML content"}), 500

    all_items = get_all_titles_parts_and_sections(root)
    matches = search_query(main_query, all_items)

    if len(matches) == 0:
        response = {"result": "Try to be more Specific on Query"}
    else:
        selected_element = matches[0]["element"]
        if selected_element:
            selected_content = display_selected_element(selected_element)
            response = {"result": selected_content, "current_date": current_date}
        else:
            response = {"error": "No content found"}
            return jsonify(response), 400

    # Handle compare part
    
    if compare_date:
        compare_root = load_xml(compare_date)
        if compare_root is None:
            return jsonify({"error": f"Failed to load XML content for the comparison date: {compare_date}"}), 500

        compare_items = get_all_titles_parts_and_sections(compare_root)
        compare_matches = search_query(main_query, compare_items)

        if not compare_matches:
            response["comparison"] = "No matches found for the comparison date."
        else:
            # Retrieve the most relevant comparison content
            compare_content = None
            for match in compare_matches:
                compare_content = display_selected_element(match["element"])
                break  # Since we've sorted matches, the first one should be the best

            if compare_content:
                response["comparison"] = compare_content
            else:
                response["comparison"] = "No exact match found for the comparison date."
    
    return jsonify(response)

@api_compare_bp.route('/available_dates', methods=['GET'])
def get_available_dates():
    try:
        container_client = blob_service_client.get_container_client(container_name)
        blobs = container_client.list_blobs()
        
        dates = set()
        for blob in blobs:
            parts = blob.name.split('/')
            if len(parts) > 1:
                date_str = parts[0]
                try:
                    # Validate date format
                    datetime.strptime(date_str, '%Y-%m-%d')
                    dates.add(date_str)
                except ValueError:
                    continue
        
        # Return dates sorted in reverse chronological order
        return jsonify({"dates": sorted(dates, reverse=True)})
    
    except AzureError as e:
        return jsonify({"error": f"Error fetching dates from Azure Blob Storage: {e}"}), 500
