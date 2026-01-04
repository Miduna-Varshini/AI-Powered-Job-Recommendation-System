import streamlit as st
import pandas as pd
import pickle
import os

# ---------------------------------
# Page config
# ---------------------------------
st.set_page_config(
    page_title="AI Career Eligibility Checker",
    page_icon="🧠",
    layout="centered"
)

# ---------------------------------
# Custom CSS
# ---------------------------------
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
.main {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
}
h1 {
    color: #2c3e50;
}
.skill-box {
    background-color: #ecf0f1;
    padding: 8px 12px;
    border-radius: 8px;
    display: inline-block;
    margin: 4px;
}
.success-box {
    background-color: #d4edda;
    padding: 15px;
    border-radius: 10px;
}
.error-box {
    background-color: #f8d7da;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# File paths
# ---------------------------------
MODEL_FILE = "knn_job_recommender.pkl"
SKILLS_FILE = "skills_list.pkl"
DATA_FILE = "career_dataset.csv"

# ---------------------------------
# File checks
# ---------------------------------
for file in [MODEL_FILE, SKILLS_FILE, DATA_FILE]:
    if not os.path.exists(file):
        st.error(f"❌ Missing file: {file}")
        st.stop()

# ---------------------------------
# Load model & data
# ---------------------------------
with open(MODEL_FILE, "rb") as f:
    knn = pickle.load(f)

with open(SKILLS_FILE, "rb") as f:
    all_skills = pickle.load(f)

df = pd.read_csv(DATA_FILE)
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
df["skills"] = df["skills"].str.lower()

# ---------------------------------
# Title
# ---------------------------------
st.title("🧠 AI Career Eligibility Checker")
st.write("Check whether you are eligible for your dream job")

# ---------------------------------
# Step 1: Job selection
# ---------------------------------
st.subheader("🎯 Select Career You Want")

career_list = sorted(df["recommended_career"].unique())
selected_career = st.selectbox(
    "Choose a career",
    career_list
)

# ---------------------------------
# Get required skills for selected career
# ---------------------------------
career_skills_text = df[df["recommended_career"] == selected_career]["skills"].iloc[0]
career_required_skills = [s.strip() for s in career_skills_text.split(",")]

st.markdown("**Required Skills:**")
for s in career_required_skills:
    st.markdown(f"<span class='skill-box'>{s}</span>", unsafe_allow_html=True)

# ---------------------------------
# Step 2: User skill input
# ---------------------------------
st.subheader("🛠 Select Your Skills")

user_vector = []
cols = st.columns(3)

for i, skill in enumerate(all_skills):
    with cols[i % 3]:
        checked = st.checkbox(skill.title())
        user_vector.append(1 if checked else 0)

# ---------------------------------
# Step 3: Eligibility check
# ---------------------------------
if st.button("🔍 Check Eligibility"):
    if sum(user_vector) == 0:
        st.warning("⚠️ Please select at least one skill")
    else:
        user_skill_names = [
            all_skills[i] for i, v in enumerate(user_vector) if v == 1
        ]

        missing_skills = [
            s for s in career_required_skills
            if s.lower() not in user_skill_names
        ]

        st.markdown("---")

        if len(missing_skills) <= 1:
            st.markdown(
                "<div class='success-box'><h3>✅ You are ELIGIBLE!</h3>"
                "<p>You match the required skill set.</p></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='error-box'><h3>❌ Not Eligible</h3>"
                "<p>You are missing the following skills:</p></div>",
                unsafe_allow_html=True
            )

            for m in missing_skills:
                st.markdown(f"- {m}")

# ---------------------------------
# Footer
# ---------------------------------
st.markdown("---")
st.caption("Final Year Project • Machine Learning • Streamlit")
