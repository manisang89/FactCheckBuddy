import os
from flask import Flask, request, render_template
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use basic model instead of gemini-pro
model = genai.GenerativeModel("models/gemini-2.0-flash-lite-001")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/check', methods=['POST'])
def check():
    claim = request.form['claim']
    prompt = f"""
    Please fact-check the following claim: "{claim}"

    Respond in this format:
    - ✅ Verdict: True / False / Partially True
    - 🧠 Reasoning: [Short explanation]
    - 🔗 Sources (if any): [Optional trusted source names or links]
    """
    try:
        response = model.generate_content(prompt)
        return render_template("result.html", claim=claim, result=response.text)
    except Exception as e:
        return f"<p>❌ Error: {e}</p>"

if __name__ == '__main__':
    app.run(debug=True)
