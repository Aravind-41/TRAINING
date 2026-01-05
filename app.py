from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    client = None
    print(f"Warning: OpenAI client not initialized: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_code():
    try:
        data = request.json
        description = data.get('description', '')
        language = data.get('language', 'python')

        if not description:
            return jsonify({'error': 'Description is required'}), 400

        prompt = f"""
Generate clean, well-documented {language} code.

Description:
{description}

Rules:
- Include docstrings/comments
- Follow best practices
- Handle errors
- Production ready
- Output ONLY code
"""

        if client is None:
            return jsonify({"error": "OpenAI client not initialized. Set OPENAI_API_KEY and ensure compatible packages are installed."}), 503

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert code generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        return jsonify({
            "code": response.choices[0].message.content,
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/explain', methods=['POST'])
def explain_code():
    try:
        data = request.json
        code = data.get('code', '')

        if not code:
            return jsonify({'error': 'Code is required'}), 400

        prompt = f"""
Explain this code clearly:

{code}

Include:
1. Purpose
2. Key parts
3. Working
4. Improvements
"""

        if client is None:
            return jsonify({"error": "OpenAI client not initialized. Set OPENAI_API_KEY and ensure compatible packages are installed."}), 503

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert code explainer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        return jsonify({
            "explanation": response.choices[0].message.content,
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)