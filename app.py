import streamlit as st
import pandas as pd
import pickle
import os

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="AI Job Eligibility & Recommendation",
    page_icon="🧠",
    layout="centered"
)

# -------------------------------------------------
# Custom CSS (responsive & visible)
# -------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #eef2f7;
    color: #1f2933;
}
.main {
    background-color: #ffffff;
    padding: 30px;
    border-radius: 14px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}
h1, h2, h3, h4 {
    color: #111827;
}
p, label, div {
    color: #1f2933 !important;
    font-size: 16px;
}
.skill-box {
    background-color: #2563eb;
    color: white;
    padding: 6px 12px;
    border-radius: 20px;
    display: inline-block;
    margin: 5px;
    font-size: 14px;
}
a.company-link {
    text-decoration: none;
    color: #2563eb;
}
button[kind="primary"] {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    padding: 10px 18px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# File paths
# -------------------------------------------------
MODEL_FILE = "knn_job_recommender.pkl"
SKILLS_FILE = "skills_list.pkl"
DATA_FILE = "career_dataset.csv"

# -------------------------------------------------
# Check files
# -------------------------------------------------
for file in [MODEL_FILE, SKILLS_FILE, DATA_FILE]:
    if not os.path.exists(file):
        st.error(f"❌ Missing file: {file}")
        st.stop()

# -------------------------------------------------
# Load model & data
# -------------------------------------------------
with open(MODEL_FILE, "rb") as f:
    knn = pickle.load(f)

with open(SKILLS_FILE, "rb") as f:
    all_skills = pickle.load(f)

df = pd.read_csv(DATA_FILE)
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Ensure optional columns exist
for col in ["skills", "domain", "company_name", "company_type"]:
    if col not in df.columns:
        df[col] = ""

df["skills"] = df["skills"].astype(str).str.lower()
df["domain"] = df["domain"].astype(str).str.title()
df["company_name"] = df["company_name"].astype(str).str.title()
df["company_type"] = df["company_type"].astype(str).str.title()

# -------------------------------------------------
# Utility function
# -------------------------------------------------
def normalize(skill):
    return skill.strip().lower().replace(" ", "")

# -------------------------------------------------
# Step 0: Signup/Login
# -------------------------------------------------
st.title("🧠 AI Job Eligibility & Recommendation")
st.subheader("🔐 Sign Up / Login")
username = st.text_input("Enter your name:")
if username:
    st.success(f"Welcome, {username}!")

# -------------------------------------------------
# Step 1: Domain selection
# -------------------------------------------------
st.subheader("🌐 Select Domain")
domain_list = sorted(df["domain"].unique())
selected_domain = st.selectbox("Choose Domain", domain_list)

# Step 2: Career selection in domain
domain_careers = sorted(df[df["domain"] == selected_domain]["recommended_career"].unique())
selected_career = st.selectbox("Select Job Role", domain_careers)

# -------------------------------------------------
# Step 3: Show Required Skills
# -------------------------------------------------
career_row = df[df["recommended_career"] == selected_career]
if career_row.empty:
    st.error("❌ No data found for this career.")
    st.stop()
else:
    career_skills_text = career_row["skills"].iloc[0]
    career_required_skills = [s.strip() for s in career_skills_text.split(",")]

    st.markdown("### 🔑 Required Skills for this Job")
    for s in career_required_skills:
        st.markdown(f"<span class='skill-box'>{s}</span>", unsafe_allow_html=True)

# -------------------------------------------------
# Step 4: User Skills Selection
# -------------------------------------------------
st.subheader("🛠 Select Your Skills")
user_vector = []
cols = st.columns(3)
for i, skill in enumerate(all_skills):
    with cols[i % 3]:
        checked = st.checkbox(skill.title())
        user_vector.append(1 if checked else 0)

# -------------------------------------------------
# Step 5: Eligibility Check
# -------------------------------------------------
if st.button("🔍 Check Eligibility"):
    if sum(user_vector) == 0:
        st.warning("⚠️ Please select at least one skill")
    else:
        user_skills = [all_skills[i] for i, v in enumerate(user_vector) if v == 1]

        required_skills_norm = [normalize(s) for s in career_required_skills]
        user_skills_norm = [normalize(s) for s in user_skills]

        matched_skills = [s for s in required_skills_norm if s in user_skills_norm]
        missing_skills = [s for s in required_skills_norm if s not in user_skills_norm]
        match_percent = (len(matched_skills) / len(required_skills_norm)) * 100

        st.markdown("---")
        st.subheader("📊 Eligibility Result")
        st.write(f"**Skill Match Percentage:** {match_percent:.2f}%")
        st.info(f"Matched {len(matched_skills)} out of {len(required_skills_norm)} required skills")

        if match_percent >= 60:
            st.success("✅ You are ELIGIBLE for this career!")
        else:
            st.error("❌ You are NOT eligible for this career")

        if missing_skills:
            st.markdown("### ❗ Skills to Improve")
            for skill in missing_skills:
                st.write("-", skill.title())

        # -------------------------------------------------
        # Step 6: Show Companies Hiring
        # -------------------------------------------------
        # -------------------------------------------------
# Step 6: Show Companies Hiring with real links
# -------------------------------------------------
        if match_percent >= 60:
            st.subheader("🏢 Companies Currently Hiring for this Role")

    # Map company names to official careers/job pages
            company_links = {
                "Wipro": "https://careers.wipro.com/",
                "Infosys": "https://www.infosys.com/careers/",
                "Amazon": "https://www.amazon.jobs/en/",
                "Zoho": "https://www.zoho.com/careers.html",
                "TCS": "https://www.tcs.com/careers",
                "Microsoft": "https://careers.microsoft.com/",
                "Google": "https://careers.google.com/",
                "IBM": "https://www.ibm.com/careers",
        # Add more companies if needed
            }
    
            hiring_companies = df[df["recommended_career"] == selected_career][["company_name", "company_type"]].drop_duplicates()

            for i, row in hiring_companies.iterrows():
                name = row["company_name"]
                ctype = row["company_type"]
                url = company_links.get(name, f"https://www.google.com/search?q={name}+careers")
                st.markdown(f"- <a class='company-link' href='{url}' target='_blank'>{name}</a> ({ctype})", unsafe_allow_html=True)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.caption("Final Year Project • Machine Learning • Streamlit")
