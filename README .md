# 🧠 AI-Powered Learning Assistant

An enhanced Streamlit-based learning assistant powered by Google's Gemini AI, designed to provide personalized tutoring across multiple subjects.

## ✨ Key Enhancements

### 1. **Professional UI/UX**
- Custom CSS styling with gradient headers
- Clean, centered layout
- Session statistics dashboard
- Responsive design

### 2. **Advanced Features**
- **Learning Modes**: Switch between different subjects (Math, Science, Programming, etc.)
- **Session Statistics**: Track messages, duration, and current mode
- **Temperature Control**: Adjust response creativity (0.0 = focused, 2.0 = creative)
- **Quick Actions**: Generate quizzes, study tips, and practice problems
- **Chat Export**: Download your learning session as a Markdown file

### 3. **Improved System Prompt**
The assistant now has specialized instructions to:
- Explain complex concepts simply
- Provide step-by-step guidance
- Encourage critical thinking
- Adapt to student's understanding level
- Use examples and analogies effectively

### 4. **Better Error Handling**
- API key validation
- Try-catch blocks for API calls
- User-friendly error messages
- Graceful degradation

### 5. **Session Management**
- Persistent chat history during session
- Message counting
- Session duration tracking
- Easy chat clearing and export

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key

### Installation

1. **Clone or download the files**

2. **Install required packages**
```bash
pip install streamlit google-generativeai python-dotenv
```

3. **Create a `.env` file** in the same directory:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

4. **Get your Gemini API key**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with your Google account
   - Create a new API key
   - Copy and paste it into your `.env` file

### Running the Application

```bash
streamlit run enhanced_learning_assistant.py
```

The app will open in your default browser at `http://localhost:8501`

## 📖 How to Use

### Basic Usage
1. Type your question in the chat input at the bottom
2. The AI will respond with detailed, educational answers
3. Continue the conversation - the AI remembers context

### Learning Modes
- Select a specific subject from the sidebar dropdown
- The AI will tailor responses to that subject area
- Modes available: General, Math, Science, Programming, Languages, History

### Quick Actions
- **Generate Quiz**: Creates a 5-question quiz on recent topics
- **Study Tips**: Get subject-specific study strategies
- **Practice Problem**: Receive a practice problem with solution

### Adjusting Creativity
- Use the "Response Creativity" slider
- Lower values (0.0-0.7): More focused, factual responses
- Higher values (0.7-2.0): More creative, varied responses

### Exporting Sessions
1. Click "Export Chat" in the sidebar
2. Download a Markdown file of your entire session
3. Review or share your learning conversation

## 🎯 Example Use Cases

### For Students
- **Homework Help**: "Explain photosynthesis in simple terms"
- **Problem Solving**: "Walk me through this calculus problem step-by-step"
- **Exam Prep**: "Generate a practice quiz for the French Revolution"

### For Self-Learners
- **Concept Exploration**: "What are the fundamentals of machine learning?"
- **Project Guidance**: "Help me plan a Python web scraping project"
- **Language Practice**: "Let's practice Spanish conversation"

### For Teachers
- **Resource Creation**: "Create 10 practice problems for algebra"
- **Explanation Ideas**: "Give me different ways to explain gravity to 5th graders"
- **Assessment Design**: "Design a rubric for evaluating research papers"

## 🛠️ Technical Details

### Models Used
- **Primary**: `gemini-2.0-flash-exp` (fast, efficient, experimental)
- Falls back to `gemini-1.5-flash` if needed

### Key Dependencies
```
streamlit>=1.28.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
```

### Session State Management
The app uses Streamlit's session state to maintain:
- Chat history
- Message count
- Session start time
- Learning mode
- UI preferences

## 🔒 Privacy & Security

- All conversations are ephemeral (not stored permanently)
- API key stored locally in `.env` file
- No data sent to third parties except Google's Gemini API
- Export feature allows you to save conversations locally

## 💡 Tips for Best Results

1. **Be Specific**: Instead of "Help with math", try "Explain quadratic equations with examples"
2. **Ask Follow-ups**: The AI remembers context, so build on previous answers
3. **Use Learning Modes**: Switch modes for subject-specific expertise
4. **Adjust Temperature**: Lower for factual topics, higher for creative subjects
5. **Export Sessions**: Save valuable learning conversations for review

## 🐛 Troubleshooting

### "API Key not found" Error
- Ensure `.env` file is in the same directory as the Python script
- Check that the file is named exactly `.env` (not `.env.txt`)
- Verify the API key format: `GOOGLE_API_KEY=AIza...`

### Slow Responses
- Try using a lower temperature setting
- Check your internet connection
- Gemini API may have rate limits on free tier

### Chat Not Clearing
- Click the "Clear Chat History" button in the sidebar
- Refresh the browser page if needed

## 🚀 Future Enhancements

Potential additions (feel free to implement):
- Voice input/output
- Image upload for visual problem-solving
- Progress tracking across sessions
- Multi-language support
- Flashcard generation
- Spaced repetition reminders

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and enhance this learning assistant for your needs!

---

**Built with ❤️ using Streamlit and Google Gemini AI**
