## 🚀 AI-Powered Excel Mock Interviewer

An AI-driven Streamlit application to simulate real-time Excel interviews, evaluate candidate answers intelligently, and provide detailed feedback — built for modern hiring workflows.

---

### 📌 Features

* ✅ **Structured Interview Flow**
  Multi-turn question and answer interface with progress tracking.

* 🧠 **AI Answer Evaluation**
  Uses OpenAI's `gpt-4o-mini` to evaluate user answers based on ideal responses.

* ⏱️ **Real-Time Countdown Timer**
  Simulates timed interview conditions (15 minutes by default).

* 📊 **Automated Feedback and Scoring**
  Assigns scores (1-5) with specific strengths and improvement areas.

* 📁 **MongoDB Integration**
  Stores questions, answers, sessions, and feedback securely.

---

### 🗂️ Folder Structure

```
📦 excel-mock-interviewer/
├── test.py                  # Main Streamlit app
├── excel_questions.csv      # Question bank (loaded at runtime)
├── requirements.txt         # Python dependencies
├── .env                     # [Only for local development]
```

---

### 🛠️ Tech Stack

* **Frontend**: [Streamlit](https://streamlit.io/)
* **Backend AI**: [OpenAI GPT-4o-mini](https://openai.com/)
* **Database**: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
* **Deployment**: [Render](https://render.com/) | (Also compatible with [GCP Cloud Run](https://cloud.google.com/run))

---

### 🧪 Local Development

#### 🔧 Prerequisites:

* Python 3.11+ recommended
* `pip install -r requirements.txt`

#### 🏃 Run it locally:

```bash
# Make sure .env exists:
# OPENAI_KEY_API=your_openai_key
# MONGODB_URI=your_mongo_uri

streamlit run test.py
```

---

### ☁️ Deployment on Render

1. Push code to GitHub
2. Create a new **Web Service** on Render:

   * Runtime: Python
   * Start command:

     ```bash
     streamlit run test.py --server.port $PORT --server.headless true
     ```
   * Add environment variables:

     * `OPENAI_KEY_API=your-openai-key`
     * `MONGODB_URI=your-mongodb-uri`
3. Add `excel_questions.csv` in the repo root so Render can load it.
4. Deploy and access your **public link**.
   https://ai-hiring-excel-interviewer.onrender.com/

### 🧠 AI Evaluation Prompt (Built-in)

> The system uses an embedded prompt that evaluates answers by checking:
>
> * Concept understanding
> * Accuracy (even with different wording)
> * Completeness against the ideal answer


### 🤝 Contribution

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

### 🛡️ License

MIT License

---


