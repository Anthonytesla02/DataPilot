from app import app

# Vercel requires the app to be available at module level
# This allows Vercel to import the Flask app directly
application = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
