# newapp.py
import streamlit as st
import pandas as pd
import bcrypt
from kb_manager import load_knowledge_base, search_knowledge_base
from database_manager import (
    get_complaints, save_complaint, get_user,
    update_complaint_status, register_user, get_user_complaints
)
from llm_handler import generate_llm_response

# Load custom CSS
try:
    with open("style.css.txt", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Custom CSS file not found. Continuing without styling.")

# Load KB once
@st.cache_data
def load_data():
    return load_knowledge_base()

KB_DATA = load_data()

# Session defaults
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.page = "home"

if "messages" not in st.session_state:
    st.session_state.messages = {}

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# ---------------- Homepage ----------------
def homepage():
    st.markdown(
        """
        <div class="homepage-container">
            <div class="homepage-header">
                <h1>🎓 Student HelpDesk Portal</h1>
                <p>Your one-stop solution for college information and support</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤 Student Portal", use_container_width=True):
            st.session_state.page = "user_login"
            st.rerun()
        st.caption("Access chatbot, submit complaints, and get help")
    with col2:
        if st.button("⚙️ Admin Portal", use_container_width=True):
            st.session_state.page = "admin_login"
            st.rerun()
        st.caption("Manage complaints and monitor system")

# ---------------- Student Login ----------------
def user_login_page():
    st.title("Student Portal 🔒")
    st.markdown("---")
    col1, col2 = st.columns([1,1])
    with col1:
        st.header("📱 Student Login")
        with st.form("student_login"):
            student_username = st.text_input("Username", key="s_user")
            student_password = st.text_input("Password", type="password", key="s_pass")
            submit_student = st.form_submit_button("Log In as Student")
            if submit_student:
                user = get_user(student_username)
                if user and check_password(student_password, user["password_hash"]) and user["role"] == "student":
                    st.session_state.logged_in = True
                    st.session_state.role = "student"
                    st.session_state.username = student_username
                    st.session_state.page = "student"
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

    with col2:
        st.header("✨ New Student Sign Up")
        with st.form("student_signup"):
            new_username = st.text_input("Choose Username")
            new_email = st.text_input("College Email (@pvpsit.ac.in)")
            new_password = st.text_input("Choose Password", type="password")
            signup_submit = st.form_submit_button("Create Student Account")
            if signup_submit:
                if not new_email.endswith('@pvpsit.ac.in'):
                    st.error("Invalid email domain. Use @pvpsit.ac.in")
                elif register_user(new_username, new_email, new_password, "student"):
                    st.success("Account created! Please log in.")
                else:
                    st.error("Username or email already exists.")

# ---------------- Admin Login ----------------
def admin_login_page():
    st.title("Admin Portal 🔒")
    st.markdown("---")
    col1, col2 = st.columns([1,1])
    with col1:
        st.header("⚙️ Admin Login")
        with st.form("admin_login"):
            admin_username = st.text_input("Username", key="a_user")
            admin_password = st.text_input("Password", type="password", key="a_pass")
            submit_admin = st.form_submit_button("Log In as Admin")
            if submit_admin:
                user = get_user(admin_username)
                if user and check_password(admin_password, user["password_hash"]) and user["role"] == "admin":
                    st.session_state.logged_in = True
                    st.session_state.role = "admin"
                    st.session_state.username = admin_username
                    st.session_state.page = "admin"
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
    with col2:
        st.header("🔧 Admin Sign Up")
        with st.form("admin_signup"):
            admin_new_username = st.text_input("Admin Username")
            admin_new_email = st.text_input("Admin Email (@pvpsiddhartha.ac.in)")
            admin_new_password = st.text_input("Admin Password", type="password")
            admin_signup_submit = st.form_submit_button("Create Admin Account")
            if admin_signup_submit:
                if not admin_new_email.endswith('@pvpsiddhartha.ac.in'):
                    st.error("Invalid email domain. Use @pvpsiddhartha.ac.in")
                elif register_user(admin_new_username, admin_new_email, admin_new_password, "admin"):
                    st.success("Admin account created! Please log in.")
                else:
                    st.error("Username or email exists.")
def student_page():
    # Header and logout/new chat buttons
    col1, col2 = st.columns([3,1])
    with col1:
        st.title(f"Hello, {st.session_state.username}! 👋")
        st.subheader("Welcome to your Student HelpDesk")
    with col2:
        if st.button("🔄 New Chat", key="new_chat"):
            # Only clear the active chat, keep history
            if st.session_state.username in st.session_state.messages:
                st.session_state.messages[st.session_state.username] = []
            st.rerun()
        if st.button("🚪 Logout", key="logout"):
            st.session_state.clear()
            st.session_state.page = "home"
            st.rerun()

    st.markdown("---")

    # --- Resolved Complaints ---
    resolved_complaints = get_user_complaints(st.session_state.username, status="resolved")
    if resolved_complaints:
        st.subheader("🎉 Resolved Complaints")
        for complaint in resolved_complaints:
            with st.expander(f"Complaint ID: {complaint[0]}", expanded=True):
                st.success(f"**Issue Type:** {complaint[2]}\n**Description:** {complaint[3]}\n**Admin Response:** {complaint[5]}")
                if st.button("Mark as Read", key=f"read_{complaint[0]}"):
                    # Update complaint as 'read'
                    update_complaint_status(complaint[0], "read", complaint[5])
                    st.experimental_rerun()

    # Ensure messages container exists
    if st.session_state.username not in st.session_state.messages:
        st.session_state.messages[st.session_state.username] = []

    # Tabs for Chatbot, Complaints, and History
    tab_chatbot, tab_complaint, tab_history = st.tabs(["🤖 Chatbot", "📝 Complaint Box", "📜 Chat History"])

    # --- Chatbot ---
    with tab_chatbot:
        st.header("💬 Chat with HelpBot")

        # Static search box at top
        query = st.text_input("Ask me anything about the college...", key="chat_input")

        # Handle user query submission
        if query:
            # Append user query to active chat
            st.session_state.messages[st.session_state.username].append({"role":"user","content":query})

            with st.spinner("🤔 Thinking..."):
                try:
                    answer = search_knowledge_base(query, KB_DATA)
                    if answer and "I'm still learning" not in answer:
                        response = answer
                    else:
                        response = generate_llm_response(query, KB_DATA)
                except Exception as e:
                    print(f"LLM Error: {e}")
                    answer = search_knowledge_base(query, KB_DATA)
                    response = answer if answer else "Sorry, I could not find an answer."

            # Append assistant response
            st.session_state.messages[st.session_state.username].append({"role":"assistant","content":response})

        # Display chat: left=assistant, right=user
        for msg in st.session_state.messages[st.session_state.username]:
            left, right = st.columns([3,3])
            if msg["role"] == "assistant":
                with left:
                    st.markdown(f"**Assistant:** {msg['content']}")
            else:
                with right:
                    st.markdown(f"**You:** {msg['content']}")

    # --- Complaint Box ---
    with tab_complaint:
        st.header("📋 Submit Complaint")
        with st.form("complaint_form", clear_on_submit=True):
            student_name = st.text_input("Your Name (Optional)", value=st.session_state.username)
            issue_type = st.selectbox("Type of Issue", ["Ragging", "Harassment", "Infrastructure", "Academics", "Other"])
            description = st.text_area("Describe the issue", placeholder="Details...")
            submitted = st.form_submit_button("Submit Complaint")
            if submitted:
                if description.strip():
                    save_complaint(student_name, issue_type, description)
                    st.success("✅ Complaint submitted securely.")
                else:
                    st.error("Please provide a description.")

    # --- Chat History ---
    with tab_history:
        st.header("📜 Your Chat History")
        full_history = get_user_complaints(st.session_state.username)
        # Display chat messages (active + past)
        if st.session_state.messages[st.session_state.username]:
            for i, message in enumerate(st.session_state.messages[st.session_state.username]):
                with st.expander(f"Message {i+1}: {message['content'][:50]}...", expanded=False):
                    st.write(f"**Role:** {message['role']}")
                    st.write(f"**Content:** {message['content']}")
        else:
            st.info("No chat history yet.")


# ---------------- Admin Page ----------------
def admin_page():
    st.title("📊 Admin Dashboard")
    st.subheader("Complaint Management System")
    col1, col2 = st.columns([3,1])
    with col2:
        if st.button("🚪 Logout", key="admin_logout"):
            st.session_state.clear()
            st.session_state.page = "home"
            st.rerun()

    st.markdown("---")
    complaints = get_complaints()
    active_complaints = [c for c in complaints if c[5] != "read"]

    if active_complaints:
        st.metric("Active Complaints", len(active_complaints))
        for complaint in active_complaints:
            col1, col2 = st.columns([3,1])
            with col1:
                st.subheader(f"Complaint ID: {complaint[0]}")
                st.write(f"**Student:** {complaint[1] if complaint[1] else 'Anonymous'}")
                st.write(f"**Type:** {complaint[2]}")
                st.write(f"**Status:** {complaint[5]}")
                st.text_area("Description", value=complaint[3], height=100, key=f"desc_{complaint[0]}", disabled=True)
            with col2:
                with st.form(key=f"form_{complaint[0]}"):
                    new_status = st.selectbox("Update Status", ["pending","in progress","resolved"], key=f"status_{complaint[0]}")
                    admin_response = st.text_area("Response", placeholder="Enter response...", key=f"response_{complaint[0]}")
                    if st.form_submit_button("Update Complaint"):
                        if new_status == "resolved" and not admin_response.strip():
                            st.error("Provide a response when resolving.")
                        else:
                            update_complaint_status(complaint[0], new_status, admin_response)
                            st.success("Complaint updated.")
                            st.rerun()
            st.markdown("---")
    else:
        st.success("🎉 All complaints addressed.")
        st.info("No active complaints found.")




# ---------------- Main Navigation ----------------
if st.session_state.page == "home":
    homepage()
elif not st.session_state.logged_in:
    if st.session_state.page == "user_login":
        user_login_page()
    elif st.session_state.page == "admin_login":
        admin_login_page()
    else:
        homepage()
else:
    if st.session_state.role == "student":
        student_page()
    elif st.session_state.role == "admin":
        admin_page()

# Back button
if not st.session_state.logged_in and st.session_state.page != "home":
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()


