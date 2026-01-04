import streamlit as st
import pandas as pd
import pickle
import os

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="AI Powered Job Recommendation System",
    page_icon="🧠",
    layout="centered"
)

# -------------------------------------------------
# CSS (VISIBLE + RESPONSIVE)
# -------------------------------------------------
st.markdown("""
<style>
body { background-color: #eef2f7; color: #111827; }

.main {
    background-color: white;
    padding: 30px;
    border-radius: 14px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
}

h1, h2, h3 { color: #111827; }

.skill {
    background: #2563eb;
    color: white;
    padding: 6px 14px;
    border-radius: 20px;
    margin: 4px;
    display: inline-block;
    font-size: 14px;
}

.company-card {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Load files
# -------------------------------------------------
DATA_FILE = "career_dataset.csv"
COMPANY_FILE = "company_jobs.csv"
SKILLS_FILE = "skills_list.pkl"

for f in [DATA_FILE, COMPANY_FILE, SKILLS_FILE]:
    if not os.path.exists(f):
        st.error(f"❌ Missing file: {f}")
        st.stop()

df = pd.read_csv(DATA_FILE)
companies = pd.read_csv(COMPANY_FILE)

with open(SKILLS_FILE, "rb") as f:
    all_skills = pickle.load(f)

df.columns = df.columns.str.lower()
companies.columns = companies.columns.str.lower()

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def normalize(x):
    return x.strip().lower().replace(" ", "")

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("🧠 AI Powered Job Recommendation System")
st.write("Skill-based eligibility & company job matching")

# -------------------------------------------------
# STEP 1: Domain Selection
# -------------------------------------------------
st.subheader("📌 Choose Domain")

domains = sorted(companies["domain"].unique())
selected_domain = st.selectbox("Select your domain", domains)

domain_jobs = companies[companies["domain"] == selected_domain]

# -------------------------------------------------
# STEP 2: Job Role
# -------------------------------------------------
st.subheader("🎯 Choose Job Role")

job_roles = sorted(domain_jobs["job_role"].unique())
selected_role = st.selectbox("Select job role", job_roles)

job_data = domain_jobs[domain_jobs["job_role"] == selected_role]

# -------------------------------------------------
# Required Skills
# -------------------------------------------------
required_skills = job_data.iloc[0]["required_skills"].split(",")

st.markdown("### 🔑 Required Skills")
for s in required_skills:
    st.markdown(f"<span class='skill'>{s.strip()}</span>", unsafe_allow_html=True)

# -------------------------------------------------
# STEP 3: User Skills
# -------------------------------------------------
st.subheader("🛠 Select Your Skills")

user_skills = []
cols = st.columns(3)

for i, skill in enumerate(all_skills):
    with cols[i % 3]:
        if st.checkbox(skill.title()):
            user_skills.append(skill.lower())

# -------------------------------------------------
# STEP 4: Eligibility + Company Matching
# -------------------------------------------------
if st.button("🔍 Check Eligibility & Jobs"):
    if not user_skills:
        st.warning("⚠️ Please select at least one skill")
        st.stop()

    req_norm = [normalize(s) for s in required_skills]
    user_norm = [normalize(s) for s in user_skills]

    matched = [s for s in req_norm if s in user_norm]
    match_percent = (len(matched) / len(req_norm)) * 100

    st.markdown("---")
    st.subheader("📊 Eligibility Result")
    st.write(f"**Skill Match:** {match_percent:.2f}%")

    if match_percent >= 60:
        st.success("✅ You are ELIGIBLE for this job")
    else:
        st.error("❌ You are NOT eligible for this job")

    # -------------------------------------------------
    # Companies Hiring
    # -------------------------------------------------
    st.markdown("---")
    st.subheader("🏢 Companies Hiring")

    for _, row in job_data.iterrows():
        comp_req = [normalize(s) for s in row["required_skills"].split(",")]
        comp_match = len([s for s in comp_req if s in user_norm])
        comp_percent = (comp_match / len(comp_req)) * 100

        st.markdown(f"""
        <div class="company-card">
            <h4>{row['company']} ({row['type']})</h4>
            <p><b>Job:</b> {row['job_role']}</p>
            <p><b>Eligibility:</b> {"✅ Eligible" if comp_percent >= 60 else "❌ Not Eligible"}</p>
            <p><b>Match:</b> {comp_percent:.2f}%</p>
            <a href="{row['apply_link']}" target="_blank">🔗 Apply Now</a>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.caption("Final Year Project • AI Job Recommendation System • Streamlit")
