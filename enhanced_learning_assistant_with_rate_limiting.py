import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
from datetime import datetime
import time
from google.api_core import exceptions

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI-Powered Learning Assistant",
    page_icon='🧠',
    layout="centered",
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("⚠️ GOOGLE_API_KEY not found! Please add it to your .env file.")
    st.stop()

try:
    gen_ai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"Failed to configure Gemini API: {str(e)}")
    st.stop()

# System prompt
SYSTEM_PROMPT = """You are an expert AI Learning Assistant designed to help students learn effectively. Your role is to:

1. Explain complex concepts in simple, understandable terms
2. Provide step-by-step guidance for problem-solving
3. Encourage critical thinking by asking thought-provoking questions
4. Adapt your teaching style to the student's level of understanding
5. Use examples, analogies, and visual descriptions when helpful
6. Break down large topics into manageable chunks
7. Provide practice problems and quizzes when appropriate
8. Offer study tips and learning strategies

Always be patient, encouraging, and supportive."""

# Auto-detect available models
@st.cache_resource
def get_available_models():
    """Get list of available models that support generateContent"""
    try:
        models = []
        for m in gen_ai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Remove 'models/' prefix
                model_name = m.name.replace('models/', '')
                models.append(model_name)
        return models
    except Exception as e:
        st.error(f"Error fetching models: {e}")
        return []

# Get available models
available_models = get_available_models()

if not available_models:
    st.error("❌ No models available for your API key.")
    st.info("""
    **Possible solutions:**
    1. Check your API key is valid at https://aistudio.google.com/app/apikey
    2. Generate a new API key
    3. Make sure the Gemini API is enabled for your project
    4. Update google-generativeai: `pip install --upgrade google-generativeai`
    """)
    st.stop()

# Initialize session state
if "chat_session" not in st.session_state:
    # Use the first available model
    default_model = available_models[0]
    
    try:
        model = gen_ai.GenerativeModel(
            model_name=default_model,
            system_instruction=SYSTEM_PROMPT
        )
        st.session_state.chat_session = model.start_chat(history=[])
        st.session_state.current_model = default_model
        st.session_state.message_count = 0
        st.session_state.session_start = datetime.now()
        st.session_state.last_request_time = 0
        st.session_state.request_count = 0
        st.session_state.rate_limit_hit = False
    except Exception as e:
        st.error(f"Error initializing model: {e}")
        st.stop()

if "learning_mode" not in st.session_state:
    st.session_state.learning_mode = "General"

if "show_stats" not in st.session_state:
    st.session_state.show_stats = True

# Rate limiting configuration
MIN_REQUEST_INTERVAL = 2.0
MAX_RETRIES = 3
RETRY_DELAY = 5

def send_message_with_retry(chat_session, message, max_retries=MAX_RETRIES):
    """Send message to Gemini with automatic retry on rate limit errors"""
    for attempt in range(max_retries):
        try:
            # Check rate limiting
            current_time = time.time()
            time_since_last_request = current_time - st.session_state.last_request_time
            
            if time_since_last_request < MIN_REQUEST_INTERVAL:
                wait_time = MIN_REQUEST_INTERVAL - time_since_last_request
                time.sleep(wait_time)
            
            # Send the message
            response = chat_session.send_message(message)
            
            # Update request tracking
            st.session_state.last_request_time = time.time()
            st.session_state.request_count += 1
            st.session_state.rate_limit_hit = False
            
            return response
            
        except exceptions.ResourceExhausted:
            st.session_state.rate_limit_hit = True
            
            if attempt < max_retries - 1:
                wait_time = RETRY_DELAY * (2 ** attempt)
                st.warning(f"⏳ Rate limit reached. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                raise exceptions.ResourceExhausted(
                    f"Rate limit exceeded after {max_retries} attempts. Please wait a moment and try again."
                )
        
        except Exception as e:
            raise e

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Show available models
    st.subheader("📱 Available Models")
    st.success(f"✅ Found {len(available_models)} model(s)")
    
    # Model selector - show actual available models
    if len(available_models) > 1:
        selected_model = st.selectbox(
            "Choose Model",
            available_models,
            index=available_models.index(st.session_state.current_model) if st.session_state.current_model in available_models else 0
        )
        
        # Update model if changed
        if selected_model != st.session_state.current_model:
            try:
                model = gen_ai.GenerativeModel(
                    model_name=selected_model,
                    system_instruction=SYSTEM_PROMPT
                )
                st.session_state.chat_session = model.start_chat(history=[])
                st.session_state.current_model = selected_model
                st.success(f"✅ Switched to {selected_model}")
                st.rerun()
            except Exception as e:
                st.error(f"Error switching model: {e}")
    else:
        st.info(f"Using: {st.session_state.current_model}")
    
    st.divider()
    
    # Learning mode selector
    learning_mode = st.selectbox(
        "Learning Mode",
        ["General", "Math", "Science", "Programming", "Languages", "History"],
        index=["General", "Math", "Science", "Programming", "Languages", "History"].index(st.session_state.learning_mode)
    )
    
    if learning_mode != st.session_state.learning_mode:
        st.session_state.learning_mode = learning_mode
    
    st.divider()
    
    # Session stats
    st.subheader("📊 Session Info")
    st.info(f"""
    **Model:** {st.session_state.current_model}
    **Requests:** {st.session_state.request_count}
    **Mode:** {st.session_state.learning_mode}
    """)
    
    if st.session_state.rate_limit_hit:
        st.warning("⚠️ Rate limit recently hit")
    
    st.divider()
    
    # Quick actions
    st.subheader("📚 Quick Actions")
    
    if st.button("📝 Generate Quiz", use_container_width=True):
        quiz_prompt = f"Generate a 5-question quiz about our recent discussion in {learning_mode}."
        st.session_state.pending_message = quiz_prompt
        st.rerun()
    
    if st.button("💡 Study Tips", use_container_width=True):
        tips_prompt = f"Provide 5 effective study tips for {learning_mode}."
        st.session_state.pending_message = tips_prompt
        st.rerun()
    
    if st.button("🎯 Practice Problem", use_container_width=True):
        practice_prompt = f"Give me a practice problem for {learning_mode} at an intermediate level."
        st.session_state.pending_message = practice_prompt
        st.rerun()
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
        model = gen_ai.GenerativeModel(
            model_name=st.session_state.current_model,
            system_instruction=SYSTEM_PROMPT
        )
        st.session_state.chat_session = model.start_chat(history=[])
        st.session_state.message_count = 0
        st.session_state.session_start = datetime.now()
        st.session_state.request_count = 0
        st.session_state.rate_limit_hit = False
        st.rerun()
    
    st.divider()
    
    # Export chat
    if st.button("📥 Export Chat", use_container_width=True):
        chat_export = f"# Learning Session Export\n\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        chat_export += f"Model: {st.session_state.current_model}\n"
        chat_export += f"Mode: {st.session_state.learning_mode}\n\n"
        
        for message in st.session_state.chat_session.history:
            role = "Student" if message.role == "user" else "Assistant"
            chat_export += f"## {role}:\n{message.parts[0].text}\n\n"
        
        st.download_button(
            label="Download Chat",
            data=chat_export,
            file_name=f"learning_session_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True
        )

# Main content
st.markdown('<h1 class="main-header">🧠 AI-Powered Learning Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; margin-bottom: 2rem;">Your personal tutor for any subject</p>', unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Handle pending messages from quick actions
if "pending_message" in st.session_state:
    user_prompt = st.session_state.pending_message
    del st.session_state.pending_message
    
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message_with_retry(st.session_state.chat_session, user_prompt)
                st.markdown(response.text)
                st.session_state.message_count += 1
    except exceptions.ResourceExhausted:
        st.error("❌ **Rate Limit Exceeded** - Please wait 1-2 minutes before sending another message.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# Chat input
user_prompt = st.chat_input("Ask me anything about your studies...")

if user_prompt:
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message_with_retry(st.session_state.chat_session, user_prompt)
                st.markdown(response.text)
                st.session_state.message_count += 1
                
    except exceptions.ResourceExhausted:
        st.error("❌ **Rate Limit Exceeded**")
        st.info("Please wait 1-2 minutes before trying again. Free tier: 15 requests/minute.")
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# Footer
st.divider()
st.markdown('<p style="text-align: center; color: #666; font-size: 0.9rem;">Powered by Google Gemini AI | Built with Streamlit</p>', unsafe_allow_html=True)
