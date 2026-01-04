import streamlit as st
import pandas as pd
import pickle
import os

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="AI Career Eligibility Checker",
    page_icon="🧠",
    layout="centered"
)

# -------------------------------------------------
# Custom CSS (VISIBLE + RESPONSIVE)
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
df["skills"] = df["skills"].astype(str).str.lower()

# -------------------------------------------------
# Utility function
# -------------------------------------------------
def normalize(skill):
    return skill.strip().lower().replace(" ", "")

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("🧠 AI Career Eligibility Checker")
st.write("Check whether you are eligible for your dream career")

# -------------------------------------------------
# Step 1: Career selection
# -------------------------------------------------
st.subheader("🎯 Select Your Desired Career")

career_list = sorted(df["recommended_career"].unique())
selected_career = st.selectbox("Choose a career", career_list)

# -------------------------------------------------
# Required skills for selected career
# -------------------------------------------------
career_skills_text = df[df["recommended_career"] == selected_career]["skills"].iloc[0]
career_required_skills = [s.strip() for s in career_skills_text.split(",")]

st.markdown("### 📌 Required Skills")
for s in career_required_skills:
    st.markdown(f"<span class='skill-box'>{s}</span>", unsafe_allow_html=True)

# -------------------------------------------------
# Step 2: User skills
# -------------------------------------------------
st.subheader("🛠 Select Your Skills")

user_vector = []
cols = st.columns(3)

for i, skill in enumerate(all_skills):
    with cols[i % 3]:
        checked = st.checkbox(skill.title())
        user_vector.append(1 if checked else 0)

# -------------------------------------------------
# Step 3: Eligibility Check
# -------------------------------------------------
if st.button("🔍 Check Eligibility"):
    if sum(user_vector) == 0:
        st.warning("⚠️ Please select at least one skill")
    else:
        # User skills
        user_skills = [
            all_skills[i]
            for i, v in enumerate(user_vector) if v == 1
        ]

        required_skills = [s.lower() for s in career_required_skills]

        # Normalize
        user_skills_norm = [normalize(s) for s in user_skills]
        required_skills_norm = [normalize(s) for s in required_skills]

        # Match logic
        matched_skills = [
            required_skills[i]
            for i, s in enumerate(required_skills_norm)
            if s in user_skills_norm
        ]

        missing_skills = [
            required_skills[i]
            for i, s in enumerate(required_skills_norm)
            if s not in user_skills_norm
        ]

        match_percent = (len(matched_skills) / len(required_skills)) * 100

        st.markdown("---")
        st.subheader("📊 Eligibility Result")

        st.write(f"**Skill Match Percentage:** {match_percent:.2f}%")
        st.info(f"Matched {len(matched_skills)} out of {len(required_skills)} required skills")

        if match_percent >= 60:
            st.success("✅ You are ELIGIBLE for this career!")
        else:
            st.error("❌ You are NOT eligible for this career")

        if missing_skills:
            st.markdown("### ❗ Skills to Improve")
            for skill in missing_skills:
                st.write("-", skill.title())

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.caption("Final Year Project • Machine Learning • Streamlit")
