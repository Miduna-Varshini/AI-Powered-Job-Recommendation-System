import streamlit as st
import pandas as pd
import pickle
import os
import webbrowser

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="AI Powered Job Recommendation",
    page_icon="🧠",
    layout="centered"
)

# -----------------------------
# CSS for better visibility
# -----------------------------
st.markdown("""
<style>
body {background-color: #eef2f7; color: #1f2933;}
h1,h2,h3,h4 {color: #111827;}
.skill-box {background-color: #2563eb; color:white; padding:6px 12px; border-radius:20px; display:inline-block; margin:5px; font-size:14px;}
.company-box {background-color:#16a34a; color:white; padding:6px 12px; border-radius:12px; display:inline-block; margin:3px; font-size:14px;}
button[kind="primary"] {background-color: #2563eb; color:white; border-radius:8px; padding:10px 18px;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# File paths
# -----------------------------
MODEL_FILE = "knn_job_recommender.pkl"
SKILLS_FILE = "skills_list.pkl"
DATA_FILE = "career_dataset.csv"

# -----------------------------
# Check files
# -----------------------------
for file in [MODEL_FILE, SKILLS_FILE, DATA_FILE]:
    if not os.path.exists(file):
        st.error(f"❌ Missing file: {file}")
        st.stop()

# -----------------------------
# Load model & data
# -----------------------------
with open(MODEL_FILE, "rb") as f:
    knn = pickle.load(f)

with open(SKILLS_FILE, "rb") as f:
    all_skills = pickle.load(f)

df = pd.read_csv(DATA_FILE)
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
df["skills"] = df["skills"].astype(str).str.lower()

# -----------------------------
# Normalize function
# -----------------------------
def normalize(skill):
    return skill.strip().lower().replace(" ", "")

# -----------------------------
# Domain → Job Role mapping
# -----------------------------
DOMAINS = {
    "Data Science": ["Data Scientist", "ML Engineer", "AI Researcher", "Business Analyst"],
    "Web Development": ["Web Developer", "Frontend Developer", "Backend Developer"],
    "Business": ["Business Analyst", "Project Manager"]
}

# -----------------------------
# Job Role → Companies mapping with links
# -----------------------------
COMPANIES = {
    "Data Scientist": {"Wipro":"https://careers.wipro.com","Infosys":"https://www.infosys.com/careers","TCS":"https://www.tcs.com/careers","Amazon":"https://www.amazon.jobs/en/","Google":"https://careers.google.com/"},
    "ML Engineer": {"Google":"https://careers.google.com/","Microsoft":"https://careers.microsoft.com/","IBM":"https://www.ibm.com/employment/","Amazon":"https://www.amazon.jobs/en/","Wipro":"https://careers.wipro.com"},
    "AI Researcher": {"OpenAI":"https://openai.com/careers","Google DeepMind":"https://deepmind.com/careers","Microsoft":"https://careers.microsoft.com/","IBM":"https://www.ibm.com/employment/"},
    "Web Developer": {"Zoho":"https://www.zoho.com/careers.html","Freshworks":"https://www.freshworks.com/company/careers/","Microsoft":"https://careers.microsoft.com/","Amazon":"https://www.amazon.jobs/en/"},
    "Business Analyst": {"Infosys":"https://www.infosys.com/careers","Accenture":"https://www.accenture.com/us-en/careers","Deloitte":"https://www2.deloitte.com/global/en/careers","Zoho":"https://www.zoho.com/careers.html"},
    "Project Manager": {"TCS":"https://www.tcs.com/careers","IBM":"https://www.ibm.com/employment/","Microsoft":"https://careers.microsoft.com/","Infosys":"https://www.infosys.com/careers"}
}

# -----------------------------
# App Title
# -----------------------------
st.title("🧠 AI Powered Job Recommendation System")
st.write("Check your eligibility & see companies hiring!")

# -----------------------------
# Step 1: Choose Domain
# -----------------------------
st.subheader("📌 Choose Domain")
selected_domain = st.selectbox("Select your domain", list(DOMAINS.keys()))

# -----------------------------
# Step 2: Choose Job Role
# -----------------------------
st.subheader("🎯 Choose Job Role")
job_roles = DOMAINS[selected_domain]
selected_career = st.selectbox("Select job role", job_roles)

# -----------------------------
# Step 3: Show Required Skills
# -----------------------------
career_skills_text = df[df["recommended_career"] == selected_career]["skills"].iloc[0]
career_required_skills = [s.strip() for s in career_skills_text.split(",")]

st.markdown("### 🔑 Required Skills")
for s in career_required_skills:
    st.markdown(f"<span class='skill-box'>{s}</span>", unsafe_allow_html=True)

# -----------------------------
# Step 4: User Skill Input
# -----------------------------
st.subheader("🛠 Select Your Skills")
user_vector = []
cols = st.columns(3)

for i, skill in enumerate(all_skills):
    with cols[i % 3]:
        checked = st.checkbox(skill.title())
        user_vector.append(1 if checked else 0)

# -----------------------------
# Step 5: Eligibility Check
# -----------------------------
if st.button("✅ Check Eligibility"):
    if sum(user_vector) == 0:
        st.warning("⚠️ Please select at least one skill!")
    else:
        user_skills = [all_skills[i] for i, v in enumerate(user_vector) if v == 1]
        required_skills = [s.lower() for s in career_required_skills]

        user_skills_norm = [normalize(s) for s in user_skills]
        required_skills_norm = [normalize(s) for s in required_skills]

        matched_skills = [required_skills[i] for i,s in enumerate(required_skills_norm) if s in user_skills_norm]
        missing_skills = [required_skills[i] for i,s in enumerate(required_skills_norm) if s not in user_skills_norm]

        match_percent = (len(matched_skills) / len(required_skills)) * 100

        st.markdown("---")
        st.subheader("📊 Eligibility Result")
        st.write(f"**Skill Match Percentage:** {match_percent:.2f}%")
        st.info(f"Matched {len(matched_skills)} out of {len(required_skills)} skills")

        if match_percent >= 60:
            st.success("✅ You are ELIGIBLE for this career!")
            st.subheader("🏢 Companies Hiring")
            hiring_companies = COMPANIES.get(selected_career, {})
            if hiring_companies:
                for company, link in hiring_companies.items():
                    st.markdown(f"<a href='{link}' target='_blank'><span class='company-box'>{company}</span></a>", unsafe_allow_html=True)
            else:
                st.info("No company data available for this role yet.")
        else:
            st.error("❌ You are NOT eligible for this career")

        # Missing skills
        if missing_skills:
            st.markdown("### ❗ Skills to Improve")
            for skill in missing_skills:
                st.write("-", skill.title())

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Final Year Project • Machine Learning • Streamlit")
