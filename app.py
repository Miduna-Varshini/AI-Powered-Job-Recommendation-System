# app.py

import streamlit as st
import pickle
import pandas as pd

# ------------------------------
# Load model and skills list
# ------------------------------
@st.cache_data
def load_model():
    with open("knn_job_recommender.pkl", "rb") as f:
        knn_model = pickle.load(f)
    with open("skills_list.pkl", "rb") as f:
        skills_list = pickle.load(f)
    return knn_model, skills_list

knn, skills = load_model()

# ------------------------------
# Load job titles
# ------------------------------
@st.cache_data
def load_job_titles():
    df = pd.read_csv("DataScientist.csv")  # Your Kaggle dataset CSV
    # Clean column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df = df[['job_title', 'job_description']]
    df.dropna(inplace=True)
    return df['job_title']

job_titles = load_job_titles()

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("🧠 AI-Powered Job Recommendation System")
st.write("Select your skills below:")

# Skill selection
user_input = []
for skill in skills:
    val = st.checkbox(skill.title())  # Show as checkbox
    user_input.append(1 if val else 0)

# Button to recommend jobs
if st.button("Get Job Recommendations"):
    if sum(user_input) == 0:
        st.warning("Please select at least one skill!")
    else:
        # Predict using KNN
        distances, indices = knn.kneighbors([user_input])
        st.success("✅ Recommended Jobs:")
        for i in indices[0]:
            st.write("-", job_titles.iloc[i])
