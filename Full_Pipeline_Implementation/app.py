
import streamlit as st
import pandas as pd
import random
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from models.github_model import run_github_model
from models.stackoverflow_model import run_stackoverflow_model

# --- CONFIGURATION ---
ASSESSMENT_APP_URL = "http://localhost:8502"  # Ensure assessment.py runs on this port
DB_FILE = "exams_db.csv"

# !!! REPLACE THESE WITH YOUR DETAILS !!!
SENDER_EMAIL = "anishamol.gaware@srh-heidelberg.org" 
SENDER_APP_PASSWORD = "xizf dmpb mlyo avjf" # 16-char App Password (Not your login password)

st.set_page_config(layout="wide", page_title="Tech Screener Pro")
st.title("HUSHHUSH RECRUITER")

# --- EMAIL LOGIC ---
def send_email_invitation(to_email, candidate_name, link, score):
    subject = "Coding Assessment Invitation - HushHush Recruiter"
    
    html_body = f"""
    <html>
      <body>
        <h2>Hello {candidate_name},</h2>
        <p>You have been shortlisted based on your technical profile (Score: {score:.2f}).</p>
        <p>Please complete the coding assessment at the link below:</p>
        <p>
            <a href="{link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                Start Assessment
            </a>
        </p>
        <p>Or copy this link: {link}</p>
        <br>
        <p>Best regards,<br>HushHush Recruitment Team</p>
      </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'html'))

    try:
        # Using Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True, "Email sent successfully!"
    except Exception as e:
        return False, f"Failed to send: {str(e)}"

# --- DATA HELPERS ---
def assign_emails(df, score_col):
    # Sort so top scorer is first
    df = df.sort_values(by=score_col, ascending=False).reset_index(drop=True)
    
    # Generate fake emails for everyone initially
    emails = [f"candidate{random.randint(1000,9999)}@gmail.com" for _ in range(len(df))]
    
    # --- UPDATED LOGIC: Top 5 get the specific email ---
    target_email = "gawareanish@yahoo.com"
    
    # Assign target email to up to top 5 candidates
    limit = min(5, len(df))
    for i in range(limit):
        emails[i] = target_email
    
    df['email'] = emails
    return df

def load_exam_results():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["username", "source", "model_score", "exam_score", "status"])

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["🐙 GitHub", "💬 StackOverflow", "🏆 Exam Results"])

# ---------------- GitHub ----------------
with tab1:
    file = st.file_uploader("Upload GitHub CSV", type="csv", key="gh_up")
    if file:
        df = pd.read_csv(file)
        with st.spinner("Running GitHub model..."):
            result = run_github_model(df)
            # Add Email Logic
            result = assign_emails(result, 'GTS')

        st.dataframe(result, use_container_width=True)

        # Action: Send Link
        st.subheader("📧 Send Assessment Links")
        
        selected_user = st.selectbox("Select Candidate to Email", result['username'])
        
        if st.button("Send Email to Selected User", key="gh_btn"):
            user_row = result[result['username'] == selected_user].iloc[0]
            email = user_row['email']
            score = user_row['GTS']
            
            # Generate Link
            link = f"{ASSESSMENT_APP_URL}/?username={selected_user}&source=GitHub&score={score:.2f}"
            
            with st.spinner(f"Sending email to {email}..."):
                success, msg = send_email_invitation(email, selected_user, link, score)
            
            if success:
                st.success(f"✅ {msg} -> Sent to {email}")
            else:
                st.error(f"❌ {msg}")
                st.info("Check your SENDER_EMAIL and APP_PASSWORD in app.py")

# ---------------- StackOverflow ----------------
with tab2:
    file = st.file_uploader("Upload StackOverflow CSV", type="csv", key="so_up")
    if file:
        df = pd.read_csv(file)
        with st.spinner("Running StackOverflow model..."):
            result = run_stackoverflow_model(df)
            # Add Email Logic
            result = assign_emails(result, 'SOTS')

        st.dataframe(result, use_container_width=True)

        # Action: Send Link
        st.subheader("📧 Send Assessment Links")
        
        selected_user_so = st.selectbox("Select Candidate to Email", result['username'], key="so_sel")
        
        if st.button("Send Email to Selected User", key="so_btn"):
            user_row = result[result['username'] == selected_user_so].iloc[0]
            email = user_row['email']
            score = user_row['SOTS']
            
            # Generate Link
            link = f"{ASSESSMENT_APP_URL}/?username={selected_user_so}&source=StackOverflow&score={score:.2f}"
            
            with st.spinner(f"Sending email to {email}..."):
                success, msg = send_email_invitation(email, selected_user_so, link, score)
            
            if success:
                st.success(f"✅ {msg} -> Sent to {email}")
            else:
                st.error(f"❌ {msg}")
                st.info("Check your SENDER_EMAIL and APP_PASSWORD in app.py")

# ---------------- Exam Results ----------------
with tab3:
    st.header("📊 Final Assessment Report")
    st.markdown("This table aggregates data from the CSV Model and the external Coding Platform.")
    
    if st.button("Refresh Results"):
        st.rerun()
        
    results_df = load_exam_results()
    
    if not results_df.empty:
        st.dataframe(
            results_df.style.highlight_max(axis=0, subset=['exam_score'], color='#90EE90'),
            use_container_width=True
        )
        
        st.download_button(
            "⬇ Download Final Report",
            results_df.to_csv(index=False),
            "final_candidates_report.csv",
            "text/csv"
        )
    else:
        st.info("No exams completed yet. Send a link from the GitHub/SO tabs and complete a test.")
 