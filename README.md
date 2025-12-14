📄 Chat with PDF (Gemini RAG App)
<img width="1206" height="724" alt="Screen Shot 2025-12-14 at 12 52 40 PM" src="https://github.com/user-attachments/assets/170713a8-cd16-40f8-b20d-ced7701dc95d" />
<img width="1208" height="745" alt="Screen Shot 2025-12-14 at 12 53 05 PM" src="https://github.com/user-attachments/assets/f6272634-fa38-4dd2-979c-f6ed8605ee59" />
<img width="1213" height="727" alt="Screen Shot 2025-12-14 at 12 53 26 PM" src="https://github.com/user-attachments/assets/a9c15d37-b538-4168-9020-14d50abfc7f2" />
<img width="1208" height="771" alt="Screen Shot 2025-12-14 at 12 53 46 PM" src="https://github.com/user-attachments/assets/e2fb5adb-1fff-484a-8b0f-c12c62dd8bd7" />


🌟 Project Overview
This is a complete, fully-functional web application that allows users to perform Retrieval-Augmented Generation (RAG) over their PDF documents. The app uses the Google Gemini API for both contextual understanding (LLM) and embedding, providing highly accurate, source-grounded answers.

Built with minimal code complexity using Streamlit for the frontend and Embedchain for the robust RAG pipeline.

✨ Key Features
Gemini Integration: Utilizes the powerful gemini-2.5-flash model for chat and gemini-embedding-001 for vectorization.

Dynamic RAG Pipeline: Upload any PDF document to instantly create a private knowledge base.

Custom UI/UX: Features a dark-themed Streamlit interface with a background image and an interactive sidebar for settings.

Session Management: Uses Streamlit's session state to manage the conversation, LLM settings, and allows for a full application reset.

Simple Setup: Requires only a single environment variable (your Gemini API Key) to run.

🛠️ Technology Stack
Language Model (LLM): Google Gemini API (gemini-2.5-flash)

RAG/Framework: Embedchain

Vector Store: ChromaDB (local, temporary instance)

Web Framework: Streamlit

Language: Python

🚀 Setup and Installation
Prerequisites
Python 3.8+

A valid Gemini API Key.

Installation Steps
Clone the repository:

Bash

git clone https://github.com/RAVISH78981/Chat_with_Pdf_gemini.git
Create and activate a virtual environment:

Bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install dependencies: This project requires streamlit, embedchain, and the necessary Google libraries.

Bash

pip install streamlit embedchain google-generativeai
Run the application:

Bash

streamlit run chat_with_pdf_gemini.py
Usage: Enter your Gemini API key in the app's text input box, upload a PDF, and start chatting!
