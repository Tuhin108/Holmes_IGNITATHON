import os
import json
import logging
import traceback
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Debug: Check environment variables
print("=== ENVIRONMENT CHECK ===")
hf_token = os.getenv('HF_TOKEN')
print(f"HF_TOKEN exists: {bool(hf_token)}")
if hf_token:
    print(f"HF_TOKEN starts with: {hf_token[:10]}...")

# Try importing OpenAI with error handling
try:
    from openai import OpenAI
    print("✅ OpenAI imported successfully")
    
    if hf_token:
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=hf_token,
        )
        print("✅ OpenAI client created successfully")
    else:
        print("❌ No HF_TOKEN - client not created")
        client = None
        
except ImportError as e:
    print(f"❌ Failed to import OpenAI: {e}")
    client = None
except Exception as e:
    print(f"❌ Failed to create OpenAI client: {e}")
    client = None

MODEL = "openai/gpt-oss-120b:cerebras"

# Professional prompts for business-ready interviews
PROFESSIONAL_GENERATE_PROMPT = """You are a senior technical interviewer at a Fortune 500 technology company. Generate exactly 6 comprehensive interview questions for the role of "{role}".

Create questions that demonstrate enterprise-level assessment standards suitable for senior-level technical positions.

Return exactly this JSON structure with these 6 types in order:

[
  {{"type": "Aptitude", "question": "Complex analytical reasoning question testing problem-solving skills and logical thinking for {role} role"}},
  {{"type": "CodeCompletion", "question": "Practical coding task: [Task description] Complete this code: [code snippet] Expected output: [expected result]"}},
  {{"type": "TrickyCoding", "question": "Advanced algorithmic challenge: [Problem statement] Write complete solution. Expected output: [specific output]"}},
  {{"type": "TechCodeCompletion", "question": "Technology-specific task for {role}: [Task] Complete this {role}-specific code: [code] Expected: [output]"}},
  {{"type": "Technical", "question": "Deep technical knowledge question about {role} concepts, system design, or architecture"}},
  {{"type": "HR", "question": "Leadership and professional growth question: How would you handle [specific scenario relevant to {role}]?"}}
]

Requirements:
- Questions must be comprehensive and professional
- Suitable for senior-level candidates  
- Focused on real-world business applications
- Each question should be detailed and clear

Return ONLY the JSON array. No markdown, no explanations."""

PROFESSIONAL_EVALUATE_PROMPT = """Evaluate this interview response professionally:

Question: {question}
Answer: {answer}

Provide assessment in this JSON format:
{{
  "feedback": "Constructive feedback (50-70 words max)",
  "score": <integer 0-10>
}}

Focus on: technical accuracy, problem-solving approach, communication clarity."""

def extract_json_from_response(text):
    """Extract clean JSON from model response with robust error handling."""
    try:
        # Handle None input
        if not text:
            return None
            
        # Remove markdown formatting and clean up
        text = text.replace('```json', '').replace('```', '').strip()
        
        # Find JSON boundaries
        start_idx = -1
        for i, char in enumerate(text):
            if char in ['{', '[']:
                start_idx = i
                break
        
        if start_idx == -1:
            return None
        
        # Count brackets to find end - with better handling for nested structures
        bracket_count = 0
        open_char = text[start_idx]
        close_char = '}' if open_char == '{' else ']'
        in_string = False
        escape_next = False
        
        for i in range(start_idx, len(text)):
            char = text[i]
            
            if escape_next:
                escape_next = False
                continue
                
            if char == '\\':
                escape_next = True
                continue
                
            if char == '"' and not escape_next:
                in_string = not in_string
                continue
                
            if not in_string:
                if char == open_char:
                    bracket_count += 1
                elif char == close_char:
                    bracket_count -= 1
                    if bracket_count == 0:
                        json_str = text[start_idx:i+1]
                        # Try to parse to validate
                        json.loads(json_str)
                        return json_str
        
        # If we get here, try the entire remaining text
        json_str = text[start_idx:]
        try:
            json.loads(json_str)
            return json_str
        except:
            # Last resort: try to fix common JSON issues
            return fix_truncated_json(json_str)
            
    except Exception as e:
        logger.error(f"Error extracting JSON: {e}")
        return None

def fix_truncated_json(json_str):
    """Attempt to fix common JSON truncation issues."""
    try:
        # Remove any incomplete last element
        json_str = json_str.strip()
        
        # If it's an array, make sure it ends properly
        if json_str.startswith('['):
            # Find the last complete object
            last_complete = -1
            bracket_count = 0
            in_string = False
            escape_next = False
            
            for i, char in enumerate(json_str):
                if escape_next:
                    escape_next = False
                    continue
                    
                if char == '\\':
                    escape_next = True
                    continue
                    
                if char == '"' and not escape_next:
                    in_string = not in_string
                    continue
                    
                if not in_string:
                    if char == '{':
                        bracket_count += 1
                    elif char == '}':
                        bracket_count -= 1
                        if bracket_count == 0:
                            last_complete = i
            
            if last_complete > 0:
                # Truncate to last complete object and close array
                fixed = json_str[:last_complete+1] + ']'
                try:
                    json.loads(fixed)
                    return fixed
                except:
                    pass
        
        return None
    except:
        return None

def call_gpt_model(messages, max_tokens=1000, temperature=0.1):
    """Make API call to GPT-OSS-120B."""
    if not client:
        raise RuntimeError("OpenAI client not configured. Check HF_TOKEN.")
    
    try:
        logger.info(f"Making API call to {MODEL} with max_tokens={max_tokens}")
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        
        response_content = completion.choices[0].message.content
        
        # Log response details for debugging
        logger.info(f"API call successful. Response length: {len(response_content) if response_content else 0}")
        
        # Check if response was truncated by looking at finish_reason
        finish_reason = completion.choices[0].finish_reason
        logger.info(f"Finish reason: {finish_reason}")
        
        if finish_reason == 'length':
            logger.warning("Response was truncated due to max_tokens limit")
        
        if not response_content:
            logger.warning("API returned empty response")
            return ""
        
        return response_content
        
    except Exception as e:
        logger.error(f"Model API call failed: {e}")
        logger.error(f"Exception type: {type(e).__name__}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        # Re-raise the exception instead of returning None
        raise RuntimeError(f"API call failed: {str(e)}")

@app.route('/')
def index():
    """Render the main page with your styled template."""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Template error: {e}")
        return jsonify({
            "error": "Template not found",
            "message": "Please ensure templates/index.html exists",
            "details": str(e)
        }), 500

@app.route('/interview')
def interview():
    """Render the interview page with your styled template."""
    try:
        return render_template('interview.html')
    except Exception as e:
        logger.error(f"Template error: {e}")
        return jsonify({
            "error": "Template not found", 
            "message": "Please ensure templates/interview.html exists",
            "details": str(e)
        }), 500

@app.route('/results')
def results():
    """Render the results page with your styled template."""
    try:
        return render_template('results.html')
    except Exception as e:
        logger.error(f"Template error: {e}")
        return jsonify({
            "error": "Template not found",
            "message": "Please ensure templates/results.html exists", 
            "details": str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model': MODEL,
        'hf_token_configured': bool(hf_token),
        'openai_client_ready': bool(client),
        'service': 'professional-interview-generator'
    })

@app.route('/test_api')
def test_api():
    """Test endpoint to verify API connectivity."""
    if not client:
        return jsonify({
            'error': 'OpenAI client not configured',
            'hf_token_set': bool(hf_token)
        }), 500
    
    try:
        # Simple test call
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": "Say 'API test successful'"}
            ],
            max_tokens=10,
            temperature=0,
        )
        
        response_text = completion.choices[0].message.content
        return jsonify({
            'status': 'API test successful',
            'model_response': response_text,
            'model': MODEL
        })
        
    except Exception as e:
        return jsonify({
            'error': f'API test failed: {str(e)}',
            'error_type': type(e).__name__,
            'traceback': traceback.format_exc()
        }), 500

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    """Generate professional interview questions."""
    try:
        if not client:
            return jsonify({'error': 'AI service unavailable. Please check configuration.'}), 500
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        role = data.get('role', '').strip()
        if not role:
            return jsonify({'error': 'Role is required'}), 400

        prompt = PROFESSIONAL_GENERATE_PROMPT.format(role=role)
        
        messages = [
            {
                "role": "system",
                "content": "You are a senior technical interviewer at a Fortune 500 company. Generate professional interview questions in valid JSON format only."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ]

        logger.info(f"Generating questions for role: {role}")
        
        # Try with different max_tokens values if first attempt fails
        # Increased token limits to ensure 6 complete questions are generated
        max_tokens_options = [2500, 3000, 2000, 1800]
        questions = None
        
        for max_tokens in max_tokens_options:
            try:
                logger.info(f"Attempting generation with max_tokens={max_tokens}")
                response_text = call_gpt_model(messages, max_tokens=max_tokens, temperature=0.1)
                
                logger.info(f"Raw model response length: {len(response_text)}")
                logger.info(f"Raw model response (first 200 chars): {response_text[:200]}...")
                logger.info(f"Raw model response (last 200 chars): ...{response_text[-200:]}")
                
                # Extract and parse JSON
                json_text = extract_json_from_response(response_text)
                if not json_text:
                    logger.warning(f"Failed to extract JSON with max_tokens={max_tokens}, trying next option")
                    continue
                
                logger.info(f"Extracted JSON length: {len(json_text)}")
                
                try:
                    questions = json.loads(json_text)
                    logger.info(f"Successfully parsed JSON with max_tokens={max_tokens}")
                    break
                except json.JSONDecodeError as parse_error:
                    logger.warning(f"JSON parsing failed with max_tokens={max_tokens}: {parse_error}")
                    
                    # Try alternative parsing strategies
                    alternative_json = fix_truncated_json(json_text)
                    if alternative_json:
                        try:
                            questions = json.loads(alternative_json)
                            logger.info("Successfully parsed with alternative method")
                            break
                        except:
                            logger.warning("Alternative parsing also failed, trying next max_tokens option")
                            continue
                    else:
                        logger.warning("No alternative JSON fix available, trying next max_tokens option")
                        continue
                        
            except Exception as e:
                logger.warning(f"Attempt with max_tokens={max_tokens} failed: {e}")
                continue
        
        if not questions:
            raise ValueError("Failed to generate valid questions after multiple attempts")
        
        # Validate response structure
        if not isinstance(questions, list):
            raise ValueError("Response must be a JSON array")
        
        if len(questions) < 6:
            raise ValueError(f"Expected 6 questions, got {len(questions)}")
        
        # Validate question types
        expected_types = {'Aptitude', 'CodeCompletion', 'TrickyCoding', 'TechCodeCompletion', 'Technical', 'HR'}
        found_types = {q.get('type') for q in questions if isinstance(q, dict)}
        
        if not expected_types.issubset(found_types):
            logger.warning(f"Missing question types. Found: {found_types}, Expected: {expected_types}")
        
        # Ensure each question has required fields
        for i, q in enumerate(questions):
            if not isinstance(q, dict) or 'question' not in q or 'type' not in q:
                raise ValueError(f"Question {i+1} missing required fields")
        
        logger.info(f"Successfully generated {len(questions)} questions")
        return jsonify({'questions': questions})
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        return jsonify({'error': 'Failed to parse AI response. Please try again.'}), 500
    except Exception as e:
        logger.error(f"Error in generate_questions: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to generate questions: {str(e)}'}), 500

@app.route('/evaluate', methods=['POST'])
def evaluate():
    """Evaluate candidate response professionally."""
    try:
        if not client:
            return jsonify({'error': 'AI service unavailable. Please check configuration.'}), 500
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        question = data.get('question', '').strip()
        answer = data.get('answer', '').strip()

        if not question or not answer:
            return jsonify({'error': 'Question and answer are required'}), 400

        # Truncate very long inputs to prevent token limit issues
        max_question_length = 1000
        max_answer_length = 2000
        
        if len(question) > max_question_length:
            question = question[:max_question_length] + "..."
            logger.info("Question truncated due to length")
        
        if len(answer) > max_answer_length:
            answer = answer[:max_answer_length] + "..."
            logger.info("Answer truncated due to length")

        prompt = PROFESSIONAL_EVALUATE_PROMPT.format(question=question, answer=answer)
        
        messages = [
            {
                "role": "system",
                "content": "You are a senior interviewer providing professional evaluations. Return valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        logger.info("Evaluating candidate response")
        
        # Try different max_tokens values for evaluation
        max_tokens_options = [600, 800, 400, 1000]
        evaluation = None
        
        for max_tokens in max_tokens_options:
            try:
                logger.info(f"Attempting evaluation with max_tokens={max_tokens}")
                response_text = call_gpt_model(messages, max_tokens=max_tokens, temperature=0.1)
                
                # Check if response_text is valid before proceeding
                if not response_text or len(response_text.strip()) == 0:
                    logger.warning(f"Empty response with max_tokens={max_tokens}, trying next option")
                    continue
                
                logger.info(f"Raw evaluation response length: {len(response_text)}")
                logger.info(f"Raw evaluation response: {response_text[:300]}...")
                
                # Extract and parse JSON
                json_text = extract_json_from_response(response_text)
                if not json_text:
                    logger.warning(f"Could not extract JSON with max_tokens={max_tokens}, trying next option")
                    continue
                
                try:
                    evaluation = json.loads(json_text)
                    logger.info(f"Successfully parsed evaluation JSON with max_tokens={max_tokens}")
                    break
                except json.JSONDecodeError as parse_error:
                    logger.warning(f"JSON parsing failed with max_tokens={max_tokens}: {parse_error}")
                    
                    # Try to fix the JSON
                    alternative_json = fix_truncated_json(json_text)
                    if alternative_json:
                        try:
                            evaluation = json.loads(alternative_json)
                            logger.info("Successfully parsed evaluation with alternative method")
                            break
                        except:
                            logger.warning("Alternative evaluation parsing also failed")
                            continue
                    else:
                        continue
                        
            except Exception as e:
                logger.warning(f"Evaluation attempt with max_tokens={max_tokens} failed: {e}")
                continue
        
        # If all attempts failed, provide a fallback evaluation
        if not evaluation:
            logger.warning("All evaluation attempts failed, providing fallback evaluation")
            evaluation = {
                "feedback": "Unable to generate detailed feedback due to technical issues. Please review the response manually.",
                "score": 5
            }
        
        # Validate and fix evaluation structure
        if not isinstance(evaluation, dict):
            evaluation = {"feedback": "Invalid evaluation format", "score": 5}
        
        if 'feedback' not in evaluation:
            evaluation['feedback'] = "Feedback not available due to technical issues."
        
        if 'score' not in evaluation:
            evaluation['score'] = 5
        
        # Validate and fix score
        try:
            score = int(evaluation.get('score', 5))
            evaluation['score'] = max(0, min(10, score))
        except (ValueError, TypeError):
            evaluation['score'] = 5
        
        # Ensure feedback isn't too long and is a string
        if not isinstance(evaluation.get('feedback'), str):
            evaluation['feedback'] = "Feedback format error - please try again."
        else:
            words = evaluation['feedback'].split()
            if len(words) > 100:
                evaluation['feedback'] = ' '.join(words[:100]) + '...'
        
        logger.info(f"Evaluation completed with score: {evaluation['score']}")
        return jsonify(evaluation)
        
    except Exception as e:
        logger.error(f"Error in evaluate: {e}")
        logger.error(traceback.format_exc())
        
        # Return a fallback evaluation instead of error
        fallback_evaluation = {
            "feedback": "Technical error occurred during evaluation. Please try again or review manually.",
            "score": 5
        }
        return jsonify(fallback_evaluation)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"500 Error: {error}")
    return jsonify({
        'error': 'Internal server error',
        'details': str(error)
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 7860))
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f"\n=== STARTING PROFESSIONAL INTERVIEW APP ===")
    print(f"Port: {port}")
    print(f"Debug: {debug_mode}")
    print(f"HF_TOKEN configured: {bool(hf_token)}")
    print(f"OpenAI client ready: {bool(client)}")
    print(f"Model: {MODEL}")
    print("=" * 50)
    
    # Verify templates exist
    template_files = ['index.html', 'interview.html', 'results.html']
    for template in template_files:
        template_path = os.path.join('templates', template)
        if os.path.exists(template_path):
            print(f"✅ Template found: {template}")
        else:
            print(f"❌ Template missing: {template}")
    
    print("=" * 50 + "\n")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
