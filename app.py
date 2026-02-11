import streamlit as st
import pandas as pd
from groq import Groq
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# ======================================================
# CONFIG
# ======================================================

st.set_page_config(layout="wide")
styles = getSampleStyleSheet()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role":"assistant","content":"Hi 👋 I'm your SpendSense financial copilot. Ask me anything about your expenses or planning."}
    ]

def ai(prompt):
    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}]
    )
    return r.choices[0].message.content

# ======================================================
# WELCOME PAGE
# ======================================================

if st.session_state.page == "welcome":

    st.title("💰 SpendSense AI")
    st.subheader("Founder Financial Copilot")

    st.markdown("""
Upload your yearly expense CSV to get:

✔ Monthly comparisons  
✔ Budget analysis  
✔ Next month planning  
✔ AI insights  
✔ Executive PDF reports  
""")

    file = st.file_uploader("Upload Yearly CSV", type=["csv"])

    if file:
        st.session_state.file = file
        if st.button("Start Analysis"):
            st.session_state.page = "dashboard"
            st.rerun()

    st.stop()

# ======================================================
# SAFE CSV LOAD
# ======================================================

st.session_state.file.seek(0)

try:
    df = pd.read_csv(st.session_state.file)
except:
    st.error("CSV is empty or invalid.")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Date"] = df["Date"].dt.date
df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M").astype(str)
df["Week"] = pd.to_datetime(df["Date"]).dt.to_period("W").astype(str)

rules = {
    "Salaries": ["salary","payroll","stipend"],
    "Assets": ["laptop","monitor","chair","desk"],
    "Software": ["aws","zoom","notion","github"],
    "Travel": ["flight","uber","ola"],
    "Marketing": ["ads","google","facebook"],
    "Utilities": ["wifi","electricity"]
}

def categorize(d):
    for k,v in rules.items():
        for w in v:
            if w in d.lower():
                return k
    return "Other"

df["Category"] = df["Description"].apply(categorize)

months = sorted(df["Month"].unique())

# ======================================================
# SIDEBAR CHATBOT
# ======================================================

with st.sidebar:

    st.header("🤖 AI Copilot")

    for m in st.session_state.messages:
        role = "You" if m["role"]=="user" else "AI"
        st.markdown(f"**{role}:** {m['content']}")

    with st.form("chat_form"):
        chat = st.text_input("Ask me anything")
        send = st.form_submit_button("Send")

        if send and chat.strip()!="":

            reply = ai(chat)

            st.session_state.messages.append({"role":"user","content":chat})
            st.session_state.messages.append({"role":"assistant","content":reply})

            st.rerun()

if st.sidebar.button("🔄 Upload New File"):
    st.session_state.clear()
    st.rerun()

selected_month = st.sidebar.selectbox("Select Month", months)

month_df = df[df["Month"] == selected_month]

total_spend = int(month_df["Amount"].sum())
transactions = len(month_df)
category_sum = month_df.groupby("Category")["Amount"].sum()
weekly_sum = month_df.groupby("Week")["Amount"].sum()
yearly = df.groupby("Month")["Amount"].sum()

top_category = category_sum.idxmax()

# ======================================================
# DASHBOARD
# ======================================================

st.title("📊 SpendSense Dashboard")

tab1, tab2 = st.tabs(["Overview","Planning"])

# ======================================================
# OVERVIEW TAB
# ======================================================

with tab1:

    st.subheader(f"Monthly Report — {selected_month}")

    a,b,c = st.columns(3)
    a.metric("Total Spend", f"₹{total_spend}")
    b.metric("Top Category", top_category)
    c.metric("Transactions", transactions)

    st.divider()

    col1,col2 = st.columns(2)
    col1.subheader("Yearly Monthly Comparison")
    col1.line_chart(yearly)

    col2.subheader("Category Spend")
    col2.bar_chart(category_sum)

    st.subheader("Weekly Trend")
    st.line_chart(weekly_sum)

    insight = ai(f"""
You are a CFO generating a professional monthly executive summary.

Rules:
- Use clear headings
- Use bullet points
- Strictly Do NOT use markdown symbols like ** 
- Write in clean formatted plain text
- Currency must be in Rs.

Month: {selected_month}
Total Spend: ₹{total_spend}

Category Breakdown:
{category_sum.to_string()}
""")

    st.markdown(insight)

    # ================= PDF =================

    if st.button("Download Monthly PDF"):

        doc = SimpleDocTemplate("Monthly_Report.pdf", pagesize=A4)
        story = []

        story.append(Paragraph(f"SpendSense AI — Monthly Report ({selected_month})", styles["Title"]))
        story.append(Spacer(1,10))
        story.append(Paragraph(f"Total Spend: Rs.{total_spend} ", styles["BodyText"]))
        story.append(Paragraph(f"Top Category: {top_category}", styles["BodyText"]))
        story.append(Spacer(1,10))

        table_data = [["Category","Amount (Rs.)"]]
        for k,v in category_sum.items():
            table_data.append([k,f"{int(v)}"])

        table = Table(table_data)
        table.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.grey),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("GRID",(0,0),(-1,-1),1,colors.black)
        ]))

        story.append(table)
        story.append(Spacer(1,10))
        story.append(Paragraph("<b>AI Executive Insight</b>", styles["Heading2"]))
        for line in insight.split("\n"):
            story.append(Paragraph(line, styles["BodyText"]))
            story.append(Spacer(1,5))


        doc.build(story)

        with open("Monthly_Report.pdf","rb") as f:
            st.download_button("Download PDF", f, "Monthly_Report.pdf")

# ======================================================
# PLANNING TAB
# ======================================================

with tab2:

    st.subheader("Budget Tracking")

    budget = st.number_input("Monthly Budget (₹)",0)

    if budget>0:
        diff = total_spend-budget

        c1,c2,c3 = st.columns(3)
        c1.metric("Actual", f"₹{total_spend}")
        c2.metric("Budget", f"₹{budget}")
        c3.metric("Difference", f"₹{diff}")

        review = ai(f"""
Month {selected_month}
Budget ₹{budget}
Actual ₹{total_spend}
{category_sum.to_string()}
Give budget advice in INR.
""")

        st.info(review)

    st.divider()

    st.subheader("Next Month Planning")

    s,a,m,o = st.columns(4)
    salary = s.number_input("Salaries (₹)",0)
    assets = a.number_input("Assets (₹)",0)
    marketing = m.number_input("Marketing (₹)",0)
    other = o.number_input("Other (₹)",0)

    planned = salary+assets+marketing+other
    st.metric("Planned Total", f"₹{planned}")

    if st.button("Run AI Next Month Advisor"):

        planner = ai(f"""
Current Month Spend ₹{total_spend}

Next Month Plan:
Salaries ₹{salary}
Assets ₹{assets}
Marketing ₹{marketing}
Other ₹{other}
Total ₹{planned}

Act as startup finance advisor.
Give risks and optimization in INR.
""")

        st.subheader("🤖 Next Month AI Advisor")
        st.info(planner)
