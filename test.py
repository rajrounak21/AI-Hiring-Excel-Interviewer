import streamlit as st
import pandas as pd
import uuid
from pymongo import MongoClient
import streamlit.components.v1 as components
from datetime import datetime
import openai
import json
import re
import os
import time
from dotenv import load_dotenv
load_dotenv()
uri = os.getenv("MONGODB_URI")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# ----------------- MongoDB Setup -----------------
client = MongoClient(uri)
OPENAI_API_KEY=os.getenv("OPENAI_KEY_API")
db = client["mock_interview"]
questions_col = db["interview_questions"]
sessions_col = db["sessions"]
# ----------------- Disable Copy-Paste -----------------
def secure_textarea(label, key, initial_value=""):
    components.html(f"""
        <textarea id="{key}" rows="5" style="width: 100%; font-size: 16px;" 
            onpaste="event.preventDefault();" 
            oncopy="event.preventDefault();" 
            oncut="event.preventDefault();" 
            oninput="window.parent.postMessage({{ type: 'syncAnswer', key: '{key}', value: this.value }}, '*');">
        {initial_value}
        </textarea>
        <script>
            const textarea = document.getElementById("{key}");
            textarea.onpaste = e => {{ e.preventDefault(); alert("🚫 Copy-Paste is disabled."); }};
        </script>
    """, height=150)

# ----------------- Show Greetings -----------------
def show_greetings():
    greetings = [
        "👋 Hello! Welcome to your Excel interview.",
        "⌛ Get ready, this will test your Excel skills!",
        "🚀 Your interview is starting soon..."
    ]
    if "greet_step" not in st.session_state:
        st.session_state.greet_step = 0
    if st.session_state.greet_step < len(greetings):
        st.markdown(f"### {greetings[st.session_state.greet_step]}")
        if st.button("Next"):
            st.session_state.greet_step += 1
            st.experimental_rerun()
        st.stop()

# ----------------- Real-Time Timer -----------------
def show_interview_timer(total_minutes=15):
    total_seconds = total_minutes * 60
    if "interview_start_time" not in st.session_state:
        st.session_state.interview_start_time = time.time()

    elapsed = int(time.time() - st.session_state.interview_start_time)
    remaining = total_seconds - elapsed

    if remaining <= 0:
        st.session_state.current_question_index = 9999
        st.warning("⏰ Time's up! Submitting your answers.")
        st.experimental_rerun()

    mins, secs = divmod(remaining, 60)
    st.markdown(f"⏳ **Time Remaining:** `{mins:02d}:{secs:02d}`")

# ----------------- Streamlit Session -----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.current_question_index = 0
    st.session_state.evaluation_done = False

session_id = st.session_state.session_id
current_index = st.session_state.current_question_index

# ----------------- Workflow -----------------
show_greetings()
show_interview_timer(total_minutes=15)

# ----------------- Load Questions -----------------
if questions_col.count_documents({"session_id": session_id}) == 0:
    df = pd.read_csv("excel_questions.csv")
    selected = df.sample(n=5).to_dict(orient="records")
    for q in selected:
        questions_col.insert_one({
            "session_id": session_id,
            "question": q["question"],
            "ideal_answer": q["ideal_answer"],
            "user_answer": None,
            "score": None,
            "feedback": None,
            "timestamp": datetime.utcnow()
        })
    sessions_col.insert_one({
        "session_id": session_id,
        "start_time": datetime.utcnow()
    })

questions = list(questions_col.find({"session_id": session_id}))
total_questions = len(questions)

# ----------------- Main Question Logic -----------------
if current_index < total_questions:
    current_question = questions[current_index]
    st.title(f"🧠 Question {current_index + 1} of {total_questions}")
    st.write(current_question["question"])

    answer_key = f"answer_input_{current_index}"
    existing_answer = current_question.get("user_answer", "")
    user_answer = st.text_area("✍️ Your Answer:", value=existing_answer, key=answer_key)

    if st.button("Next"):
        questions_col.update_one(
            {"_id": current_question["_id"]},
            {"$set": {"user_answer": user_answer}}
        )
        st.session_state.current_question_index += 1
        st.experimental_rerun()

# ----------------- Evaluation -----------------
elif not st.session_state.evaluation_done:
    st.success("✅ You have completed all questions!")

    if st.button("🎯 Run Evaluation"):
        answered_questions = list(questions_col.find({
            "session_id": session_id,
            "user_answer": {"$ne": None}
        }))

        prompt = "You are an Excel interviewer. ONLY return a JSON array. For each question, compare the user's answer to the ideal answer, give score 1-5 and feedback.\n\n"
        for i, q in enumerate(answered_questions, 1):
            prompt += f"Q{i}:\nQuestion: {q['question']}\nIdeal Answer: {q['ideal_answer']}\nUser Answer: {q['user_answer']}\n"

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            raw_content = response.choices[0].message.content.strip()
            match = re.search(r'(\[.*\])', raw_content, re.DOTALL)

            if match:
                eval_results = json.loads(match.group(1))
                for db_item, eval_item in zip(answered_questions, eval_results):
                    questions_col.update_one(
                        {"_id": db_item["_id"]},
                        {"$set": {
                            "score": eval_item.get("score"),
                            "feedback": eval_item.get("feedback")
                        }}
                    )
                st.session_state.evaluation_done = True
                st.success("✅ Evaluation complete!")
                st.experimental_rerun()
            else:
                st.error(f"❌ Could not parse LLM output:\n{raw_content}")
        except Exception as e:
            st.error(f"❌ LLM Evaluation failed: {e}")

# ----------------- Final Results -----------------
elif st.session_state.evaluation_done:
    st.subheader("📊 Final Results")
    evaluated = list(questions_col.find({"session_id": session_id}))
    for i, q in enumerate(evaluated, 1):
        st.markdown(f"### Question {i}")
        st.write(f"**Q:** {q['question']}")
        st.write(f"**Your Answer:** {q['user_answer']}")
        st.write(f"**Ideal Answer:** {q['ideal_answer']}")
        st.write(f"**Score:** {q.get('score', 'N/A')} / 5")
        st.write(f"**Feedback:** {q.get('feedback', 'Not available')}")
        st.markdown("---")

    # 👋 Interview Goodbye
    st.success("🎉 Congratulations on completing your Excel interview!")
    st.markdown("""
    ---
    ### 🎓 What's Next?
    - ✅ Your answers have been evaluated.
    - 📊 Feedback is shown above.
    - 🕊️ Feel free to close the tab or return to the main page.

    **Thank you for participating!** 🙏  
    **We wish you the best in your journey ahead.** 🚀
    """)
