import os
import logging
from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Enable CORS for API endpoints
CORS(app)

# Configure database URL with fallback to provided database
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://reviewpilot_user:kLQiZvLx6Hk5sOw92HO5tt7Xa9oeUEL6@dpg-d27nseogjchc738fvaf0-a.oregon-postgres.render.com/reviewpilot")
app.config["DATABASE_URL"] = DATABASE_URL

# Import routes
from routes import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
