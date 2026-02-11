# 💰 SpendSense AI — Founder Financial Copilot

SpendSense AI is a GenAI-powered financial dashboard that helps founders and teams analyze expenses, track budgets, plan future spending, and receive AI-driven insights from uploaded CSV data.

It combines data analytics with an always-available AI copilot to transform raw financial data into actionable decisions.

---

## 🚀 Features

### 📊 Expense Analytics
- Upload yearly expense CSV
- Monthly comparison dashboard
- Category-wise spending
- Weekly trends
- Top expense category detection

---

### 🤖 AI Financial Copilot
- Persistent chatbot with memory
- Context-aware responses
- Budget advice
- Cost optimization suggestions
- Financial risk insights

Powered by **Groq + LLaMA 3.1**

---

### 💰 Budget Tracking
- Set monthly budget
- Compare actual vs planned
- AI budget review

---

### 📈 Next Month Planning
- Enter planned expenses
- AI-generated financial planning guidance

---

### 📄 Executive PDF Report
- Monthly summary
- Category breakdown
- AI executive insight
- Downloadable professional report

---

## 🛠 Tech Stack

| Layer | Technology |
|------|-----------|
| Frontend | Streamlit |
| Data Processing | Pandas |
| AI Engine | Groq (LLaMA 3.1) |
| Reporting | ReportLab |
| Deployment | Streamlit Community Cloud |

---

## 📁 Project Structure
-spendsense-ai/

  │
  
  ├── app.py
  
  ├── requirements.txt
  
  └── README.md

---

## ▶ Run Locally

### 1. Clone Repository


git clone https://github.com/yourusername/spendsense-ai.git

cd spendsense-ai

### 2. Create virtual environment (optional but recommended)
python -m venv venv

## Activate virtual environment (Windows)
venv\Scripts\activate

## Activate virtual environment (Mac/Linux)
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Set Groq API Key

## Windows
setx GROQ_API_KEY "your_groq_key_here"

## Mac/Linux
export GROQ_API_KEY="your_groq_key_here"

## Restart terminal after setting the key

### 5. Run the app
streamlit run app.py

☁ Free Deployment (Streamlit Cloud – Bash Style)

### 6. Push project to GitHub (after creating repo)

git init

git add .

git commit -m "Initial commit"

git branch -M main

git remote add origin https://github.com/yourusername/spendsense-ai.git

git push -u origin main

Then:

### 7. Open Streamlit Cloud
https://share.streamlit.io

### 8. Create New App

- Select your repo
- Choose app.py

### 9. Add Secret in Streamlit Cloud (TOML format)

GROQ_API_KEY = "your_groq_key_here"

### 10. Click Deploy
📊 CSV Format
## Your CSV must look like this:

Date,Description,Amount

2024-01-05,Employee Salary,250000

2024-01-10,AWS Subscription,12000



