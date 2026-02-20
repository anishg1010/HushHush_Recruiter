import streamlit as st
import pandas as pd
import os
import io
import contextlib

# --- CONFIGURATION ---
DB_FILE = "exams_db.csv"

st.set_page_config(page_title="Coding Assessment Platform", layout="centered")

# --- QUESTIONS DATA ---
questions = [
    {
        "id": 1,
        "title": "Sum of Two Numbers",
        "desc": "Write a function `solve(a, b)` that returns the sum of a and b.",
        "template": "def solve(a, b):\n    return 0",
        "test_cases": [((1, 2), 3), ((10, -2), 8), ((0, 0), 0)]
    },
    {
        "id": 2,
        "title": "Return Square",
        "desc": "Write a function `solve(n)` that returns the square of n.",
        "template": "def solve(n):\n    return 0",
        "test_cases": [((2,), 4), ((5,), 25), ((-3,), 9)]
    },
    {
        "id": 3,
        "title": "String Length",
        "desc": "Write a function `solve(s)` that returns the length of string s.",
        "template": "def solve(s):\n    return 0",
        "test_cases": [(("hello",), 5), (("",), 0), (("a",), 1)]
    }
]

# --- HELPER: EXECUTE CODE ---
def run_code(user_code, test_cases):
    """
    WARNING: exec() is dangerous in production. 
    It allows arbitrary code execution. Use only for local demos.
    """
    score = 0
    total = len(test_cases)
    
    try:
        # Create a local namespace to run the code
        local_scope = {}
        exec(user_code, {}, local_scope)
        
        if "solve" not in local_scope:
            return 0, "Function 'solve' not found."

        solve_func = local_scope["solve"]
        
        passed = 0
        for args, expected in test_cases:
            try:
                # args is a tuple, unpack it
                result = solve_func(*args)
                if result == expected:
                    passed += 1
            except Exception:
                pass
        
        score = (passed / total) * 100
        return score, f"Passed {passed}/{total} test cases."
        
    except Exception as e:
        return 0, f"Syntax/Runtime Error: {str(e)}"

# --- MAIN UI ---
def main():
    # 1. Get User Details from URL
    query_params = st.query_params
    username = query_params.get("username", "Guest")
    source = query_params.get("source", "Unknown")
    model_score = query_params.get("score", "0")

    st.title(f"📝 Coding Assessment: {username}")
    st.info(f"Source: {source} | Original Score: {model_score}")

    if username == "Guest":
        st.error("No user detected. Please use the link generated from the Main App.")
        st.stop()

    # 2. Form for Questions
    with st.form("exam_form"):
        total_score = 0
        results_log = []

        for q in questions:
            st.subheader(f"Q{q['id']}: {q['title']}")
            st.write(q['desc'])
            
            # Unique key for each text area
            code_input = st.text_area(f"Code for Q{q['id']}", value=q['template'], height=150)
            
            # We calculate score conceptually here, but only finalize on submit
            # To simplify, we re-run logic on submit
            q['user_code'] = code_input

        submitted = st.form_submit_button("Submit Assessment")

    if submitted:
        final_exam_score = 0
        
        # Grade inputs
        for q in questions:
            s, msg = run_code(q['user_code'], q['test_cases'])
            final_exam_score += s
            results_log.append(f"Q{q['id']}: {msg}")

        # Average the score across 3 questions
        final_exam_score = round(final_exam_score / len(questions), 2)

        st.success(f"Assessment Complete! Final Score: {final_exam_score}/100")
        st.json(results_log)

        # 3. Save Results to Shared CSV
        new_record = {
            "username": username,
            "source": source,
            "model_score": model_score,
            "exam_score": final_exam_score,
            "status": "Completed"
        }

        # Load existing or create new
        if os.path.exists(DB_FILE):
            df_db = pd.read_csv(DB_FILE)
        else:
            df_db = pd.DataFrame(columns=["username", "source", "model_score", "exam_score", "status"])

        # Remove old entry for this user if exists, then append new
        df_db = df_db[df_db['username'] != username]
        df_db = pd.concat([df_db, pd.DataFrame([new_record])], ignore_index=True)
        
        df_db.to_csv(DB_FILE, index=False)
        st.balloons()
        st.write("✅ Results sent to Main App. You can close this tab.")

if __name__ == "__main__":
    main()