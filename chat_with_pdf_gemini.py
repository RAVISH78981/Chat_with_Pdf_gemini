import os
import tempfile
import streamlit as st
from embedchain import App

# --- Configuration Constants ---
BACKGROUND_IMAGE_URL = "https://media.wired.com/photos/68a39121b59f5ef91a6a233c/3:2/w_1280,c_limit/gear_adobeaipdf_GettyImages-2071491879.jpg"
DEFAULT_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "gemini-embedding-001"  # Define the dedicated embedding model

# Function to initialize the Embedchain App (MODIFIED TO INCLUDE EMBEDDER MODEL NAME)
@st.cache_resource
def embedchain_bot(db_path, api_key, model_name):
    """Initializes and caches the Embedchain App for Gemini."""
    
    # LLM config still needs the API key
    llm_config = {"api_key": api_key, "model": model_name}
    
    # Embedder config: requires the model name, but no API key (it uses the env var)
    embedder_config = {"model": EMBEDDING_MODEL} 
    
    return App.from_config(
        config={
            "llm": {"provider": "google", "config": llm_config}, 
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            # Added the specific embedding model name here
            "embedder": {"provider": "google", "config": embedder_config}, 
        }
    )

# --- CSS Injection for Background and Styling (Unchanged) ---
st.markdown(
    f"""
    <style>
        /* ... (CSS code is unchanged) ... */
        .stApp {{
            background-image: url("https://media.wired.com/photos/68a39121b59f5ef91a6a233c/3:2/w_1280,c_limit/gear_adobeaipdf_GettyImages-2071491879.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: white;  
        }}
        
        .stApp::after {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.4); 
            z-index: -1; 
        }}

        .main > div {{
            background-color: rgba(10, 10, 10, 0.75); 
            padding: 20px;
            border-radius: 15px;
            margin-top: 20px;
        }}
        
        .stTextInput > div > input, .stTextArea > div > textarea {{
            color: white !important;
            background-color: rgba(30, 30, 30, 0.85);
            border: 1px solid #4CAF50; 
        }}
        .stFileUploader > div, .stButton > button {{
            background-color: #4CAF50; 
            color: white;
            border-radius: 8px;
            font-weight: bold;
        }}
        .stSuccess {{
            background-color: rgba(76, 175, 80, 0.8); 
            color: white;
            border-radius: 10px;
            padding: 10px;
        }}
        .stSidebar {{
            background-color: rgba(30, 30, 30, 0.9);
            color: white;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar for Interactive Settings (Unchanged) ---
with st.sidebar:
    st.title("⚙️ App Settings")
    
    model_selection = st.selectbox(
        "Select Gemini Model",
        options=["gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-flash"],
        index=0,
        help="Choose the Gemini large language model for the chat."
    )

    if st.button("🗑️ Reset Application", help="Clears the chat, database, and uploaded file."):
        st.cache_resource.clear()
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    st.markdown("---")
    st.info("💡 **Tip:** Enter your API key and upload your PDF to start chatting.")


# --- Main Application Content ---
st.title("📄 AI Chat with PDF (Powered by Gemini)") 
st.subheader("An application powered by Embedchain to chat with your documents.")

# 1. API Key Input
gemini_access_token = st.text_input("Gemini API Key", type="password")

if gemini_access_token:
    # Set the API Key as an environment variable for the embedder
    os.environ["GEMINI_API_KEY"] = gemini_access_token
    
    # Use session state to manage the app instance across interactions
    if "app" not in st.session_state:
        db_path = tempfile.mkdtemp()
        st.session_state.app = embedchain_bot(db_path, gemini_access_token, model_selection)
        st.session_state.db_path = db_path
        st.session_state.pdf_uploaded = False

    app = st.session_state.app
    
    # 2. File Uploader
    pdf_file = st.file_uploader("Upload a PDF file", type="pdf", disabled=st.session_state.get("pdf_uploaded", False))

    if pdf_file and not st.session_state.pdf_uploaded:
        try:
            with st.spinner("Processing PDF and building knowledge base..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
                    f.write(pdf_file.getvalue())
                    app.add(f.name, data_type="pdf_file")
            
            os.remove(f.name)
            st.session_state.pdf_uploaded = True
            st.success(f"✅ Successfully added **{pdf_file.name}** to knowledge base! You can now ask questions.")
        except Exception as e:
            # Note: This general exception catch may hide underlying issues, but is kept for robustness
            st.error(f"An error occurred during file processing: {e}")
            
    # Display the knowledge base status
    if st.session_state.get("pdf_uploaded", False):
        st.markdown(f"**Knowledge Base Status:** 🟢 Ready to chat with your PDF!")
    else:
        st.markdown(f"**Knowledge Base Status:** 🔴 Waiting for PDF upload...")


    st.markdown("---")
    
    # 3. Chat Interface
    prompt = st.text_area("❓ **Ask a question about the PDF**", height=100)
    
    if st.button("Generate Answer", disabled=not st.session_state.get("pdf_uploaded", False)):
        if prompt:
            with st.spinner("Thinking..."):
                answer = app.chat(prompt)
                st.markdown("### 🤖 Answer")
                st.info(answer)
        else:
            st.warning("Please enter a question.")

# --- Footer ---
st.markdown("---")
st.write("Project made by Ravish Sharma")

