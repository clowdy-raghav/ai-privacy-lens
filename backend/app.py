from flask import Flask, render_template, jsonify 
from analyzer import analyze_conversations

app = Flask(__name__,
            template_folder="D:\\RAGHAV WORK\\ai-privacy-lens\\frontend",
            static_folder="D:\\RAGHAV WORK\\ai-privacy-lens\\frontend")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze")
def analyze():
    result = analyze_conversations()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)