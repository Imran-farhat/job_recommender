from flask import Flask, render_template, request, jsonify
import json
from matcher import match_jobs
from format_converter import smart_convert

app = Flask(__name__)

# Load jobs database
with open("data/jobs.json", "r") as f:
    JOBS_DB = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        # Get the raw JSON input
        raw_input = request.form["preferences"]
        
        # Use smart converter to handle any JSON format
        prefs = smart_convert(raw_input)
        
        # Get job matches
        results = match_jobs(prefs, JOBS_DB)
        
        return render_template("results.html", preferences=prefs, results=results)
    
    except ValueError as e:
        # Handle JSON conversion errors
        error_msg = f"JSON Format Error: {str(e)}"
        return render_template("index.html", error=error_msg)
    
    except Exception as e:
        # Handle other errors
        error_msg = f"Processing Error: {str(e)}"
        return render_template("index.html", error=error_msg)

@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    try:
        # For API, expect JSON directly
        if request.is_json:
            raw_data = request.get_json()
            # Convert dict to JSON string for smart converter
            raw_input = json.dumps(raw_data)
        else:
            raw_input = request.data.decode('utf-8')
        
        # Use smart converter
        prefs = smart_convert(raw_input)
        results = match_jobs(prefs, JOBS_DB)
        
        return jsonify({
            "status": "success",
            "converted_preferences": prefs,
            "results": results
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == "__main__":
    # Disable debug mode and reduce logging
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    print("🚀 Starting Smart Job Matcher...")
    print("📍 Server running at: http://127.0.0.1:5000")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(debug=False, host='127.0.0.1', port=5000)
