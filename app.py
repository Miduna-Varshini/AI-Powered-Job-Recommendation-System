import streamlit as st
import urllib.parse

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Powered Job Recommendation System",
    page_icon="💼",
    layout="centered"
)

st.title("💼 AI Powered Job Recommendation System")
st.caption("Final Year Project • Machine Learning Concept • Streamlit")

st.divider()

# -------------------------------------------------
# DOMAIN → ROLE → SKILLS
# -------------------------------------------------
domain_data = {
    "Data Science": {
        "Data Scientist": ["Python", "Machine Learning", "Statistics", "SQL"],
        "Data Analyst": ["Python", "Excel", "SQL", "Power BI"]
    },
    "Web Development": {
        "Web Developer": ["HTML", "CSS", "JavaScript", "React"],
        "Backend Developer": ["Python", "Django", "SQL", "API"]
    },
    "Software Engineering": {
        "Software Developer": ["Java", "DSA", "OOP", "SQL"],
        "Full Stack Developer": ["Java", "Spring Boot", "React", "MySQL"]
    }
}

# -------------------------------------------------
# USER INPUT
# -------------------------------------------------
domain = st.selectbox("📌 Select Domain", list(domain_data.keys()))

career = st.selectbox(
    "🎯 Select Job Role",
    list(domain_data[domain].keys())
)

required_skills = domain_data[domain][career]

user_skills = st.multiselect(
    "🛠 Select Your Skills",
    sorted({skill for roles in domain_data[domain].values() for skill in roles})
)

location = st.selectbox(
    "📍 Preferred Job Location",
    ["Madurai", "Chennai", "Bangalore", "Hyderabad", "Remote"]
)

st.divider()

# -------------------------------------------------
# ELIGIBILITY CHECK
# -------------------------------------------------
if st.button("🔍 Check Eligibility"):
    if not user_skills:
        st.warning("⚠️ Please select at least one skill.")
    else:
        matched = list(set(user_skills) & set(required_skills))
        match_percent = (len(matched) / len(required_skills)) * 100

        st.subheader("📊 Eligibility Result")
        st.write(f"**Skill Match Percentage:** {match_percent:.2f}%")

        if match_percent >= 60:
            st.success("✅ You are ELIGIBLE for this job role!")

            st.subheader("🔑 Required Skills")
            st.write(", ".join(required_skills))

            # -------------------------------------------------
            # NAUKRI JOB SEARCH LINKS
            # -------------------------------------------------
            st.subheader("🔎 Apply Jobs on Naukri")

            encoded_role = urllib.parse.quote(career.lower())
            encoded_location = urllib.parse.quote(location.lower())

            naukri_link = f"https://www.naukri.com/{encoded_role}-jobs-in-{encoded_location}"

            st.markdown(
                f"""
                🔗 **[Click here to view live {career} jobs in {location} on Naukri]({naukri_link})**
                """
            )

            st.info(
                "You will be redirected to Naukri.com where you can apply for real job openings."
            )

        else:
            st.error("❌ You are NOT eligible for this job role.")
            missing = list(set(required_skills) - set(user_skills))
            st.subheader("📌 Skills to Improve")
            st.write(", ".join(missing))

st.divider()
st.caption("© 2026 | AI Job Recommendation System")
