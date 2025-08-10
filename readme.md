# InterviewGPT 🧠⚡

**Master your next interview with AI-powered mock sessions**

## https://fox15-interviewgpt.hf.space/

InterviewGPT is a cutting-edge AI-powered interview preparation platform that generates personalized technical interview questions and provides real-time feedback to help candidates excel in their job interviews. Built with Flask and powered by advanced language models, it offers a comprehensive interview simulation experience.

![InterviewGPT Banner](https://img.shields.io/badge/InterviewGPT-AI%20Interview%20Mastery-00ffff?style=for-the-badge&logo=robot)

## ✨ Features

### 🎯 Core Functionality
- **Dynamic Question Generation**: AI generates 6 comprehensive interview questions tailored to specific roles
- **Multi-Question Categories**: 
  - Aptitude & Problem-Solving
  - Code Completion Challenges
  - Advanced Algorithmic Problems
  - Technology-Specific Tasks
  - Technical Architecture Questions
  - HR & Leadership Scenarios
- **Real-Time Voice Recognition**: Advanced speech-to-text capabilities for natural interview simulation
- **AI-Powered Evaluation**: Intelligent scoring and detailed feedback for each response
- **Manual Input Fallback**: Text-based input option for broader browser compatibility

### 🚀 User Experience
- **Immersive UI/UX**: Cyberpunk-inspired design with dynamic animations and effects
- **Progressive Web App**: Responsive design optimized for all devices
- **Real-Time Progress Tracking**: Visual progress indicators and session management
- **Comprehensive Results**: Detailed performance analytics and improvement suggestions
- **Professional Reporting**: Printable results with detailed question-by-question breakdown

### 🔧 Technical Excellence
- **Enterprise-Grade Architecture**: Built with Flask for scalability and reliability
- **Advanced Error Handling**: Robust error recovery and user feedback mechanisms
- **Session Management**: Secure client-side session storage with data validation
- **API Integration**: Seamless integration with Hugging Face's inference endpoints
- **Browser Compatibility**: Support for modern web browsers with graceful degradation

## 🛠️ Technology Stack

### Backend
- **Flask** - Lightweight WSGI web application framework
- **Python 3.8+** - Core programming language
- **OpenAI SDK** - Integration with language models via Hugging Face
- **python-dotenv** - Environment variable management

### Frontend
- **HTML5/CSS3** - Modern web standards with advanced CSS features
- **Vanilla JavaScript** - Pure JavaScript for optimal performance
- **Web Speech API** - Browser-native speech recognition
- **CSS Grid/Flexbox** - Responsive layout systems
- **CSS Animations** - Hardware-accelerated animations

### AI/ML Integration
- **GPT-OSS-120B** - Advanced language model via Cerebras
- **Hugging Face Inference** - Cloud-based model serving
- **Custom Prompt Engineering** - Optimized prompts for interview scenarios

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Hugging Face account with API access

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/interviewgpt.git
cd interviewgpt
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment setup**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Configure environment variables**
```env
HF_TOKEN=your_hugging_face_token_here
FLASK_DEBUG=false
PORT=7860
```

6. **Run the application**
```bash
python app.py
```

7. **Access the application**
   - Open your browser and navigate to `http://localhost:7860`
   - Start your AI-powered interview preparation!

## 📁 Project Structure

```
interviewgpt/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
└── templates/           # HTML templates
    ├── index.html       # Landing page
    ├── interview.html   # Interview interface
    └── results.html     # Results dashboard
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `HF_TOKEN` | Hugging Face API token | - | ✅ Yes |
| `FLASK_DEBUG` | Enable Flask debug mode | `false` | ❌ No |
| `PORT` | Application port | `7860` | ❌ No |

### Model Configuration

The application uses **GPT-OSS-120B** via Cerebras through Hugging Face's inference endpoints. To modify the model:

```python
MODEL = "openai/gpt-oss-120b:cerebras"  # Current model
# Can be changed to other compatible models
```

## 🎮 How to Use

### 1. Start Interview Session
- Enter your target role (e.g., "Full Stack Developer", "Data Scientist")
- Click "Initialize AI Session" to generate personalized questions

### 2. Answer Questions
- **Voice Mode**: Click the microphone button and speak your answer
- **Manual Mode**: Switch to text input for typing responses
- Questions cover 6 different categories for comprehensive assessment

### 3. Receive AI Feedback
- Get immediate scoring (0-10) for each answer
- Read detailed feedback on your performance
- Learn from constructive suggestions

### 4. Review Results
- View comprehensive performance analytics
- Analyze question-by-question breakdown
- Print or save results for future reference

## 🔄 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/interview` | GET | Interview interface |
| `/results` | GET | Results dashboard |
| `/generate_questions` | POST | Generate AI questions |
| `/evaluate` | POST | Evaluate user responses |

### Utility Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Application health check |
| `/test_api` | GET | API connectivity test |

## 🧪 Testing

### Health Check
```bash
curl http://localhost:7860/health
```

### API Test
```bash
curl http://localhost:7860/test_api
```

### Manual Testing Flow
1. Navigate to the landing page
2. Enter a test role (e.g., "Software Engineer")
3. Complete the interview simulation
4. Verify results page functionality

## 🛡️ Error Handling

The application implements comprehensive error handling:

- **API Failures**: Graceful fallback with user-friendly messages
- **Network Issues**: Automatic retry mechanisms with exponential backoff
- **Browser Compatibility**: Feature detection and polyfills
- **Input Validation**: Client and server-side validation
- **Session Management**: Automatic cleanup and recovery

## 📊 Performance Features

### Optimization
- **Lazy Loading**: Dynamic content loading for faster initial page loads
- **Caching**: Intelligent caching of API responses
- **Compression**: Gzip compression for faster data transfer
- **Minification**: Optimized CSS and JavaScript delivery

### Monitoring
- **Logging**: Comprehensive application logging
- **Error Tracking**: Detailed error reporting and stack traces
- **Performance Metrics**: Response time and throughput monitoring

## 🔒 Security Considerations

- **Input Sanitization**: All user inputs are properly sanitized
- **CSRF Protection**: Built-in Flask CSRF protection
- **API Key Security**: Environment-based configuration
- **Client-Side Storage**: Secure session management
- **Error Information**: No sensitive data in error messages

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

#### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 7860
CMD ["python", "app.py"]
```

#### Heroku Deployment
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### Environment Variables for Production
```env
HF_TOKEN=your_production_token
FLASK_DEBUG=false
PORT=80
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Standards
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings for functions
- Include error handling
- Write unit tests

### Areas for Contribution
- Additional question categories
- Multi-language support
- Advanced analytics
- Mobile app development
- Performance optimizations

## 📋 Requirements

### System Requirements
- Python 3.8+
- 2GB+ RAM
- Modern web browser
- Internet connection for AI inference

### Python Dependencies
```txt
Flask==2.3.3
python-dotenv==1.0.0
openai==1.3.0
requests==2.31.0
```

## 🐛 Troubleshooting

### Common Issues

**Q: Speech recognition not working**
- Ensure you're using HTTPS or localhost
- Check browser permissions for microphone access
- Try the manual input option as fallback

**Q: API errors during question generation**
- Verify your Hugging Face token is valid
- Check internet connectivity
- Monitor API rate limits

**Q: Questions not displaying properly**
- Clear browser cache and cookies
- Check browser console for JavaScript errors
- Ensure sessionStorage is enabled

**Q: Slow response times**
- Check network connectivity
- Monitor Hugging Face API status
- Consider using a different model endpoint

## 📚 Documentation

### Additional Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Hugging Face API Guide](https://huggingface.co/docs/api-inference/index)
- [Web Speech API Reference](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face** for providing world-class AI inference infrastructure
- **Cerebras** for the powerful GPT-OSS-120B model
- **Flask Community** for the excellent web framework
- **Open Source Community** for inspiration and continuous improvement

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/interviewgpt/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/interviewgpt/discussions)
- **Email**: support@interviewgpt.com

---

<div align="center">
  
**InterviewGPT - Where AI meets Interview Excellence** 🚀

[![Made with ❤️ by Developer](https://img.shields.io/badge/Made%20with%20❤️-by%20Developer-red.svg)](https://github.com/yourusername)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![AI Powered](https://img.shields.io/badge/AI-Powered-purple.svg)](https://huggingface.co)

</div>
