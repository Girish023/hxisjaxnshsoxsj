from flask import Flask
from FDA_Home_Page_API import api_home_bp
from FDA_Compare_API import api_compare_bp
from FDA_Notification_API import api_notification_bp
from FDA_Recent_Changes_API import api_recent_changes_bp
from FDA_ASK_API import api_ask_bp
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(api_home_bp, url_prefix='/home')
app.register_blueprint(api_compare_bp, url_prefix='/compare')
app.register_blueprint(api_notification_bp, url_prefix='/notification')
app.register_blueprint(api_recent_changes_bp, url_prefix='/recent_changes')
app.register_blueprint(api_ask_bp, url_prefix='/ask')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
