import streamlit as st
import pandas as pd
import os

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="AI Powered Job Recommendation System",
    page_icon="🧠",
    layout="centered"
)

# -------------------------------------------------
# CSS (Clean & Visible)
# -------------------------------------------------
st.markdown("""
<style>
body { background-color: #f1f5f9; }

.main {
    background-color: white;
    padding: 30px;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.skill {
    background: #2563eb;
    color: white;
    padding: 6px 14px;
    border-radius: 18px;
    margin: 5px;
    display: inline-block;
    font-size: 14px;
}

.company-card {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Load Data
# -------------------------------------------------
DATA_FILE = "company_jobs.csv"

if not os.path.exists(DATA_FILE):
    st.error("❌ company_jobs.csv not found")
    st.stop()

df = pd.read_csv(DATA_FILE)
df.columns = df.columns.str.lower()

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
# STEP 1: DOMAIN
# -------------------------------------------------
st.subheader("📌 Choose Domain")

domains = sorted(df["domain"].unique())
selected_domain = st.selectbox("Select your domain", domains)

domain_df = df[df["domain"] == selected_domain]

# -------------------------------------------------
# STEP 2: JOB ROLE
# -------------------------------------------------
st.subheader("🎯 Choose Job Role")

job_roles = sorted(domain_df["job_role"].unique())
selected_role = st.selectbox("Select job role", job_roles)

job_df = domain_df[domain_df["job_role"] == selected_role]

# -------------------------------------------------
# REQUIRED SKILLS
# -------------------------------------------------
required_skills = job_df.iloc[0]["required_skills"].split(",")

st.subheader("🔑 Required Skills")
for s in required_skills:
    st.markdown(f"<span class='skill'>{s.strip()}</span>", unsafe_allow_html=True)

# -------------------------------------------------
# USER SKILLS
# -------------------------------------------------
st.subheader("🛠 Select Your Skills")

all_skills = sorted(
    set(",".join(df["required_skills"]).split(","))
)

user_skills = []
cols = st.columns(3)

for i, skill in enumerate(all_skills):
    with cols[i % 3]:
        if st.checkbox(skill.title()):
            user_skills.append(skill.lower())

# -------------------------------------------------
# ELIGIBILITY + COMPANIES
# -------------------------------------------------
if st.button("🔍 Check Eligibility & Jobs"):
    if not user_skills:
        st.warning("⚠️ Select at least one skill")
        st.stop()

    req_norm = [normalize(s) for s in required_skills]
    user_norm = [normalize(s) for s in user_skills]

    matched = [s for s in req_norm if s in user_norm]
    match_percent = (len(matched) / len(req_norm)) * 100

    st.markdown("---")
    st.subheader("📊 Eligibility Result")

    st.write(f"**Skill Match:** {match_percent:.2f}%")

    if match_percent >= 60:
        st.success("✅ You are ELIGIBLE")
    else:
        st.error("❌ You are NOT eligible")

    # -------------------------------------------------
    # COMPANIES
    # -------------------------------------------------
    st.markdown("---")
    st.subheader("🏢 Companies Hiring")

    for _, row in job_df.iterrows():
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
st.caption("Final Year Project • AI Job Recommendation System")
