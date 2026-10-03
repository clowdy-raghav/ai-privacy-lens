import json
from flask import Flask, render_template, jsonify, request 
from analyzer import analyze_conversations

app = Flask(__name__,
            template_folder="D:\\RAGHAV WORK\\ai-privacy-lens\\frontend",
            static_folder="D:\\RAGHAV WORK\\ai-privacy-lens\\frontend")

loaded_conversations = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["GET"])
def analyze():
    global loaded_conversations

    try:
        if loaded_conversations is None:
            with open("sample_data/conversations.json", "r") as file:
                conversations = json.load(file)

        else:
            conversations = loaded_conversations

        result = analyze_conversations(conversations)

        return jsonify(result)
    except Exception as error:
        print("ANALYZE ERROR:", error)
        return jsonify({
            "error": "No file was received."
        }), 500

@app.route("/upload", methods=["POST"])
def upload():
    global loaded_conversations

    try:
        if "file" not in request.files:
            return jsonify({
                "error": "No file uploaded."
            }), 400
        
        file = request.files["file"]

        if file.filename == "":
            return jsonify({
                "error": "No files selected."
            }), 400

        if not file.filename.lower().endswith(".json"):
            return jsonify({
                "error": "Please upload a JSON file."
            }), 400

        conversations = json.load(file)

        if not isinstance(conversations, list):
            return jsonify({
                "error": "Expected a JSON array of conversations."
            }), 400

        loaded_conversations = conversations

        return jsonify({
            "success": True,
            "conversations": len(conversations)
        })

    except json.JSONDecodeError:
        return jsonify({
            "error": "The uploaded file is not valid JSON."
        }), 400

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)