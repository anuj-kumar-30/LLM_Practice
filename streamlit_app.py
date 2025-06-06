import streamlit as st
import time
from typing import Optional
from mainV02 import AIModelManager, load_dotenv
import logging

# Configure page
st.set_page_config(
    page_title="AI Chatbot Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Custom CSS for modern styling
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    
    .stSelectbox > div > div {
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: #e3f2fd;
        color: #1565c0;
        border-bottom-right-radius: 5px;
        border-left: 4px solid #2196f3;
    }
    
    .ai-message {
        background: #f5f5f5;
        color: #424242;
        border-bottom-left-radius: 5px;
        border-left: 4px solid #757575;
    }
    
    .system-message {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        text-align: center;
        font-style: italic;
    }
    
    .sidebar .element-container {
        margin-bottom: 1rem;
    }
    
    .model-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'model_manager' not in st.session_state:
        st.session_state.model_manager = None
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = None
    if 'system_prompt_set' not in st.session_state:
        st.session_state.system_prompt_set = False
    if 'chat_started' not in st.session_state:
        st.session_state.chat_started = False

def display_model_info(config):
    """Display model information in a card format"""
    st.markdown(f"""
    <div class="model-card">
        <h4>🤖 {config.name}</h4>
        <p><strong>Model:</strong> {config.model_name}</p>
        <p><strong>Provider:</strong> {config.name}</p>
    </div>
    """, unsafe_allow_html=True)

def setup_model_selection():
    """Handle model selection in sidebar"""
    st.sidebar.markdown("## 🚀 Model Selection")
    
    # Display available models
    model_options = {}
    for key, config in AIModelManager.MODELS.items():
        model_options[f"{config.name} - {config.model_name}"] = key
    
    selected_display = st.sidebar.selectbox(
        "Choose AI Model:",
        options=list(model_options.keys()),
        help="Select the AI model you want to chat with"
    )
    
    selected_key = model_options[selected_display]
    selected_config = AIModelManager.MODELS[selected_key]
    
    # Display selected model info
    display_model_info(selected_config)
    
    return selected_key, selected_config

def setup_system_prompt():
    """Handle system prompt setup"""
    st.sidebar.markdown("## 🎭 AI Personality")
    
    prompt_options = {
        "🔥 Snarky": "You are a very snarky helpfull assistant.",
        "😊 Polite": "You are a very polite helpfull assistant.",
        "🎨 Custom": "custom"
    }
    
    selected_behavior = st.sidebar.selectbox(
        "Choose AI Behavior:",
        options=list(prompt_options.keys()),
        help="Select how the AI should behave"
    )
    
    if selected_behavior == "🎨 Custom":
        custom_behavior = st.sidebar.text_input(
            "Enter custom behavior:",
            placeholder="e.g., helpful, creative, analytical"
        )
        if custom_behavior:
            return f"You are a very {custom_behavior.strip()} helpfull assistant."
        else:
            st.sidebar.warning("Please enter a custom behavior")
            return None
    else:
        return prompt_options[selected_behavior]

def create_model_manager(config, system_prompt):
    """Create and configure model manager"""
    try:
        manager = AIModelManager(config)
        # Set system prompt manually
        manager.context = [{'role': 'system', 'content': system_prompt}]
        return manager
    except Exception as e:
        st.error(f"Error creating model manager: {e}")
        return None

def display_chat_message(role, content, avatar=None):
    """Display a chat message with styling"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    elif role == "assistant":
        st.markdown(f"""
        <div class="chat-message ai-message">
            <strong>🤖 AI:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    elif role == "system":
        st.markdown(f"""
        <div class="chat-message system-message">
            <strong>⚙️ System:</strong> {content}
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size: 3rem; font-weight: bold;">
            🤖 AI Chatbot Hub
        </h1>
        <p style="font-size: 1.2rem; color: #666; margin-top: -1rem;">
            Experience the power of multiple AI models in one place
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("# ⚙️ Configuration")
        
        # Model selection
        selected_key, selected_config = setup_model_selection()
        
        # System prompt setup
        system_prompt = setup_system_prompt()
        
        # Start chat button
        if st.button("🚀 Start Chat", use_container_width=True):
            if system_prompt:
                st.session_state.model_manager = create_model_manager(selected_config, system_prompt)
                if st.session_state.model_manager:
                    st.session_state.selected_model = selected_config.name
                    st.session_state.system_prompt_set = True
                    st.session_state.chat_started = True
                    st.session_state.messages = []
                    st.rerun()
        
        # Clear chat button
        if st.session_state.chat_started:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                if st.session_state.model_manager:
                    # Reset context with system prompt
                    system_msg = st.session_state.model_manager.context[0]
                    st.session_state.model_manager.context = [system_msg]
                st.rerun()
        
        # Chat statistics
        if st.session_state.messages:
            st.markdown("## 📊 Chat Stats")
            user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
            ai_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Your Messages", user_messages)
            with col2:
                st.metric("AI Responses", ai_messages)
    
    # Main chat interface
    if not st.session_state.chat_started:
        # Welcome screen
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                        border-radius: 20px; color: white; margin: 2rem 0;">
                <h2>🎯 Getting Started</h2>
                <p style="font-size: 1.1rem; margin: 1.5rem 0;">
                    1. Choose your AI model from the sidebar<br>
                    2. Select the AI personality<br>
                    3. Click "Start Chat" to begin<br>
                    4. Start chatting with your AI assistant!
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Display current model info
        st.info(f"🤖 Currently chatting with: **{st.session_state.selected_model}**")
        
        # Chat messages container
        chat_container = st.container()
        
        with chat_container:
            # Display chat history
            for message in st.session_state.messages:
                display_chat_message(message["role"], message["content"])
        
        # Chat input
        user_input = st.chat_input("Type your message here...", key="chat_input")
        
        if user_input:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get AI response
            with st.spinner("🤔 AI is thinking..."):
                response = st.session_state.model_manager.get_response(user_input)
            
            if response and not response.startswith("Error:"):
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.error(f"Failed to get response: {response}")
            
            st.rerun()

if __name__ == "__main__":
    main()