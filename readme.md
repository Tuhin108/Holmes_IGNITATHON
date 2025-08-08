# InterviewGPT - AI-Powered Mock Interview Platform

## Overview
InterviewGPT is a Flask-based web application that provides AI-powered mock interviews for various job roles. Users can practice interview questions with real-time AI feedback using either voice input or manual text entry.

## Features Implemented

### Core Functionality
- **Dynamic Question Generation**: AI generates 6 different types of interview questions based on user's target role
- **Multi-Modal Input**: Supports both voice recognition and manual text input
- **Real-time AI Evaluation**: Instant feedback and scoring (0-10) for each answer
- **Progress Tracking**: Visual progress bar and session management
- **Detailed Results**: Comprehensive breakdown of performance with statistics

### Question Types Generated
1. **Aptitude Question**: General reasoning and problem-solving
2. **Code Completion**: Partially written code with expected output
3. **Tricky Coding Challenge**: Full coding problem to solve
4. **Tech-Specific Code Completion**: Role-specific technical challenge
5. **Technical Theory**: Concept-based technical question
6. **HR/Behavioral**: Soft skills and behavioral assessment

### UI/UX Features
- **Cyberpunk Theme**: Modern dark theme with animated backgrounds
- **Responsive Design**: Works on desktop and mobile devices
- **Voice Recognition**: Browser-based speech-to-text functionality
- **Real-time Feedback**: Immediate AI evaluation with constructive feedback
- **Session Management**: Maintains interview state across page navigation

## Tech Stack

### Backend
- **Flask**: Python web framework
- **Google Gemini AI**: For question generation and answer evaluation
- **Python Libraries**:
  - `google-generativeai`: Gemini API integration
  - `python-dotenv`: Environment variable management
  - `flask`: Web framework

### Frontend
- **Vanilla JavaScript**: No external JS frameworks
- **HTML5**: Semantic markup with modern features
- **CSS3**: Custom animations and responsive design
- **Web Speech API**: Browser-native voice recognition

## Installation & Setup

### Prerequisites
- Python 3.7+
- Google Gemini API key

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd interviewgpt
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open browser and navigate to: `http://localhost:5000`

## File Structure
```
interviewgpt/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── templates/
│   ├── index.html        # Landing page
│   ├── interview.html    # Interview session page
│   └── results.html      # Results and analytics page
└── README.md
```

## Usage Flow

### 1. Landing Page (`/`)
- User enters target job role (e.g., "Frontend Developer")
- Click "Initialize AI Session" to generate questions
- Questions are stored in browser sessionStorage

### 2. Interview Session (`/interview`)
- Displays questions one by one with progress tracking
- Voice input via microphone or manual text input
- Real-time answer submission and AI evaluation
- Immediate feedback with score (0-10 scale)

### 3. Results Page (`/results`)
- Comprehensive performance analytics
- Question-by-question breakdown
- Overall statistics and strongest areas
- Option to print results or start new interview

## API Endpoints

### `POST /generate_questions`
Generates 6 interview questions for a specific role.
- **Input**: `{"role": "Frontend Developer"}`
- **Output**: `{"questions": [...]}`

### `POST /evaluate`
Evaluates user's answer and provides feedback.
- **Input**: `{"question": "...", "answer": "..."}`
- **Output**: `{"feedback": "...", "score": 7}`

## Key Implementation Details

### AI Integration
- Uses Google Gemini 2.5 Flash model for fast responses
- Structured prompts for consistent question generation
- JSON parsing with fallback error handling
- Score normalization (0-10 scale)

### Voice Recognition
- Web Speech API integration
- Continuous speech recognition with interim results
- Automatic fallback to manual input if not supported
- Cross-browser compatibility handling

### Session Management
- Browser sessionStorage for interview state
- Progress persistence across page navigation
- Automatic cleanup on new sessions

### Error Handling
- Graceful degradation for unsupported browsers
- API error handling with user-friendly messages
- JSON parsing validation
- Network timeout handling

## Browser Compatibility
- **Full Support**: Chrome, Edge (with voice recognition)
- **Partial Support**: Firefox, Safari (manual input only)
- **Mobile**: Responsive design works on all devices

## Future Enhancements
- [ ] Database integration for user profiles
- [ ] Advanced analytics and progress tracking
- [ ] Multiple AI model support
- [ ] Video interview simulation
- [ ] Team interview scenarios
- [ ] Industry-specific question banks

## Hackathon Implementation Notes

This project was built with focus on:
- **Rapid Development**: Clean, modular code structure
- **User Experience**: Intuitive interface with immediate feedback
- **AI Innovation**: Creative use of Gemini API for interview simulation
- **Technical Excellence**: Robust error handling and cross-browser support
- **Practical Value**: Addresses real need for interview preparation

The application demonstrates effective integration of modern web technologies with AI capabilities to create a practical tool for job interview preparation.