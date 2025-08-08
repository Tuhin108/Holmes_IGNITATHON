import os
import json
import re
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure Gemini
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# Helper: Extract first valid JSON from text
def extract_json_snippet(text):
    try:
        match = re.search(r'{.*?}', text, re.DOTALL)
        return match.group(0) if match else "{}"
    except:
        return "{}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/interview')
def interview():
    return render_template('interview.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    try:
        data = request.get_json()
        role = data.get('role', '').strip()

        if not role:
            return jsonify({'error': 'Role is required'}), 400

        prompt = f'''You are a friendly interview coach. Generate exactly six interview questions for the role "{role}":

1) An aptitude question
2) A code-completion challenge: Give a partially written code (any language), an expected output, and a short task description.
3) A tricky logic-based coding challenge: Let the user write the full code to match the expected output.
4) A tech-specific code-completion challenge (related to "{role}")
5) A technical theory/concept question
6) An HR/behavioral question

Use this exact JSON format:

[
    {{ "type": "Aptitude", "question": "..." }},
    {{ "type": "CodeCompletion", "question": "Task: ..., Code: ..., ExpectedOutput: ..." }},
    {{ "type": "TrickyCoding", "question": "Task: ..., ExpectedOutput: ..." }},
    {{ "type": "TechCodeCompletion", "question": "Task: ..., Code: ..., ExpectedOutput: ..." }},
    {{ "type": "Technical", "question": "..." }},
    {{ "type": "HR", "question": "..." }}
]

Return only valid JSON. Do not include markdown or explanations.'''

        response = model.generate_content(prompt)
        questions_json = response.text.strip()

        # Clean up markdown if present
        questions_json = questions_json.replace('```json', '').replace('```', '').strip()
        questions = json.loads(questions_json)

        expected_types = {
            'Aptitude',
            'CodeCompletion',
            'TrickyCoding',
            'TechCodeCompletion',
            'Technical',
            'HR'
        }

        found_types = {q.get('type') for q in questions}
        if not isinstance(questions, list) or not expected_types.issubset(found_types):
            raise ValueError("Missing required question types or invalid format")

        return jsonify({'questions': questions})

    except json.JSONDecodeError:
        return jsonify({'error': 'Failed to parse questions from AI response'}), 500
    except Exception as e:
        print(f"Error generating questions: {str(e)}")
        return jsonify({'error': 'Failed to generate questions. Please try again.'}), 500

@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        answer = data.get('answer', '').strip()

        if not question or not answer:
            return jsonify({'error': 'Question and answer are required'}), 400

        prompt = f'''You are an expert interviewer. Evaluate the following answer.

Question: "{question}"
Answer: "{answer}"

Provide:
- Friendly, helpful feedback (max 50 words)
- One strength and one suggestion for improvement
- A score between 0 and 10

Return ONLY this valid JSON (no markdown, no code block):

{{
  "feedback": "...",
  "score": 7
}}'''

        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        print("=== Raw Gemini response ===")
        print(raw_text)

        json_str = extract_json_snippet(raw_text)
        evaluation = json.loads(json_str)

        if 'feedback' not in evaluation or 'score' not in evaluation:
            raise ValueError("Missing 'feedback' or 'score' in evaluation")

        evaluation['score'] = max(0, min(10, int(evaluation['score'])))
        return jsonify(evaluation)

    except json.JSONDecodeError as je:
        print(f"❌ JSON parsing error: {je}")
        return jsonify({'error': 'Could not parse evaluation from AI response'}), 500
    except Exception as e:
        print(f"❌ General evaluation error: {e}")
        return jsonify({'error': 'Failed to evaluate answer. Please try again.'}), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)