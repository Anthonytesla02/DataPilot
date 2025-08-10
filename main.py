import os
from app import app

# For Render deployment, app needs to be available at module level
application = app

if __name__ == "__main__":
    # Use PORT environment variable for Render, fallback to 5000 for local dev
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
