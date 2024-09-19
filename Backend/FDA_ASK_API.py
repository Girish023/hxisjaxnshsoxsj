from flask import Flask, request, jsonify, Blueprint
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Blueprint
api_ask_bp = Blueprint('ask', __name__)
CORS(api_ask_bp, origins=["http://localhost:3000"])

# Retrieve API key, endpoint, and other settings from environment variables
api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_VERSION")
model_deployment_name = os.getenv("MODEL_DEPLOYMENT_NAME")
model_name = os.getenv("MODEL_NAME")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint, 
    api_key=api_key, 
    api_version=api_version
)

def get_answer(question):
    try:
        response = client.chat.completions.create(
            model=model_deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@api_ask_bp.route('/chatgpt', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({"error": "Question is required"}), 400

    answer = get_answer(question)
    return jsonify({"answer": answer})






