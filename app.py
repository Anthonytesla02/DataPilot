import os
import logging
from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET") or "postgresql-dumper-secret-key-12345"
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Enable CORS for API endpoints
CORS(app)

# Configure database URLs
REPLIT_DATABASE_URL = os.environ.get("DATABASE_URL")
EXTERNAL_DATABASE_URL = "postgresql://reviewpilot_user:kLQiZvLx6Hk5sOw92HO5tt7Xa9oeUEL6@dpg-d27nseogjchc738fvaf0-a.oregon-postgres.render.com/reviewpilot"

app.config["REPLIT_DATABASE_URL"] = REPLIT_DATABASE_URL
app.config["EXTERNAL_DATABASE_URL"] = EXTERNAL_DATABASE_URL
app.config["DATABASE_URL"] = REPLIT_DATABASE_URL  # Default to Replit DB

# Import routes
from routes import *


