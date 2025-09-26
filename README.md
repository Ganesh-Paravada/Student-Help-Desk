Student HelpDesk Chatbot 🏫🤖

Description:
The Student HelpDesk Chatbot is an AI-powered system designed to help students quickly access college information such as exam schedules, fees, and events, and report complaints securely and anonymously. It combines knowledge base search, local LLM fallback, and a user-friendly interface built with Streamlit. Complaints are stored securely in SQLite, and admins can manage and view them via a protected panel.

📁 Project Structure
1. app.py – Streamlit Frontend & Main Application

This is the main entry point of the application.

Handles the Streamlit UI, including tabs for:

Chatbot

Timetable

Complaint Box

Admin Panel

Collects user input (queries or complaints) and displays results.

Integrates backend modules (kb_manager.py, llm_handler.py, database_manager.py) to fetch answers or save/retrieve complaints.

Key Responsibilities:

Render UI components (chat window, complaint form, admin login)

Call backend functions for KB search and LLM responses

Display output to students in real-time

2. database_manager.py – Complaint & User Data Management

Handles all database interactions using SQLite.

Functions include:

save_complaint() – store student complaints securely

get_complaints() – retrieve complaints for admin panel

get_user() / register_user() – optional user management

update_complaint_status() – track complaint resolution

Key Responsibilities:

Ensure secure and persistent storage of complaints

Provide admin dashboard access to view and manage complaints

Handle simple user authentication if required

3. kb_manager.py – Knowledge Base Search

Manages the knowledge base (KB) of college information (courses, timetables, fees, events).

Functions include:

load_knowledge_base() – read KB files (txt/CSV) into memory

search_knowledge_base(query) – retrieve relevant answers using TF-IDF or embedding-based search

Key Responsibilities:

Quickly find answers from static college data

Reduce reliance on generative AI for known questions

Ensure fast and accurate retrieval

4. llm_handler.py – Generative AI / Fallback System

Integrates local LLM (Ollama) for unanswered queries.

Functions include:

generate_llm_response(query) – produce contextual answers when KB fails

Ensures privacy & security by running LLM locally without internet dependency

Key Responsibilities:

Provide intelligent fallback answers for complex/unseen queries

Enhance chatbot capability beyond static KB

⚡ Features

Instant answers from KB

Contextual AI responses via local LLM

Secure complaint reporting

Admin dashboard for complaint management

Streamlit-based interactive UI

🔮 Future Enhancements

Voice-based interaction (speech-to-text + text-to-speech)

WhatsApp/Telegram integration

Multi-language support (English, Telugu, Hindi)

Cloud deployment for wider accessibility

Analytics dashboard for query/complaint insights
