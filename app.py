import streamlit as st

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Powered Job Recommendation System",
    page_icon="💼",
    layout="centered"
)

st.title("💼 AI Powered Job Recommendation System")
st.caption("Final Year Project • Machine Learning • Streamlit")

st.divider()

# -------------------------------------------------
# DOMAIN → CAREER → SKILLS (STATIC = NO ERRORS)
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
# COMPANIES WITH REAL CAREER LINKS
# -------------------------------------------------
company_map = {
    "Data Scientist": [
        ("Google", "https://careers.google.com/"),
        ("Amazon", "https://www.amazon.jobs/"),
        ("Microsoft", "https://careers.microsoft.com/"),
        ("IBM", "https://www.ibm.com/careers")
    ],
    "Data Analyst": [
        ("Accenture", "https://www.accenture.com/in-en/careers"),
        ("Deloitte", "https://www2.deloitte.com/global/en/careers.html"),
        ("EY", "https://www.ey.com/en_in/careers")
    ],
    "Web Developer": [
        ("Zoho", "https://www.zoho.com/careers.html"),
        ("Freshworks", "https://www.freshworks.com/company/careers/"),
        ("Infosys", "https://www.infosys.com/careers/")
    ],
    "Backend Developer": [
        ("TCS", "https://www.tcs.com/careers"),
        ("Wipro", "https://careers.wipro.com/"),
        ("Cognizant", "https://careers.cognizant.com/")
    ],
    "Software Developer": [
        ("Google", "https://careers.google.com/"),
        ("Microsoft", "https://careers.microsoft.com/"),
        ("Amazon", "https://www.amazon.jobs/")
    ],
    "Full Stack Developer": [
        ("Accenture", "https://www.accenture.com/in-en/careers"),
        ("Zoho", "https://www.zoho.com/careers.html"),
        ("Capgemini", "https://www.capgemini.com/careers/")
    ]
}

# -------------------------------------------------
# USER INPUT
# -------------------------------------------------
domain = st.selectbox("📌 Select Domain", list(domain_data.keys()))

career = st.selectbox(
    "🎯 Select Career",
    list(domain_data[domain].keys())
)

required_skills = domain_data[domain][career]

user_skills = st.multiselect(
    "🛠 Select Your Skills",
    sorted({skill for skills in domain_data[domain].values() for skill in skills})
)

st.divider()

# -------------------------------------------------
# ELIGIBILITY CHECK
# -------------------------------------------------
if st.button("🔍 Check Eligibility"):
    if not user_skills:
        st.warning("⚠️ Please select at least one skill.")
    else:
        matched_skills = list(set(user_skills) & set(required_skills))
        match_percent = (len(matched_skills) / len(required_skills)) * 100

        st.subheader("📊 Eligibility Result")

        st.write(f"**Skill Match Percentage:** {match_percent:.2f}%")
        st.info(f"Matched {len(matched_skills)} out of {len(required_skills)} required skills")

        if match_percent >= 60:
            st.success("✅ You are ELIGIBLE for this career!")

            st.subheader("🔑 Required Skills")
            st.write(", ".join(required_skills))

            st.subheader("🏢 Companies Currently Hiring for this Role")

            companies = company_map.get(career, [])

            if companies:
                for company, link in companies:
                    st.markdown(f"- 🔗 [{company}]({link})")
            else:
                st.info("No company data available for this role.")

        else:
            st.error("❌ You are NOT eligible for this career.")
            st.subheader("📌 Improve These Skills")
            missing = list(set(required_skills) - set(user_skills))
            st.write(", ".join(missing))

st.divider()
st.caption("© 2026 Final Year Project | AI Job Recommendation System")
