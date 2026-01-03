# app.py

import streamlit as st
import pickle
import os
import pandas as pd

# ------------------------------
# Load model and skills list safely
# ------------------------------
MODEL_PATH = "knn_job_recommender.pkl"
SKILLS_PATH = "skills_list.pkl"
DATASET_PATH = "DataScientist.csv"

if not os.path.exists(MODEL_PATH) or not os.path.exists(SKILLS_PATH):
    st.error("❌ Model files not found. Make sure knn_job_recommender.pkl and skills_list.pkl are in the same folder as app.py")
    st.stop()

with open(MODEL_PATH, "rb") as f:
    knn = pickle.load(f)

with open(SKILLS_PATH, "rb") as f:
    skills = pickle.load(f)

# ------------------------------
# Load job titles
# ------------------------------
if not os.path.exists(DATASET_PATH):
    st.error(f"❌ Dataset file {DATASET_PATH} not found!")
    st.stop()

df = pd.read_csv(DATASET_PATH)
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
df = df[['job_title', 'job_description']]
df.dropna(inplace=True)
job_titles = df['job_title']

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("🧠 AI-Powered Job Recommendation System")
st.write("Select your skills below:")

# Skill selection
user_input = []
for skill in skills:
    val = st.checkbox(skill.title())
    user_input.append(1 if val else 0)

if st.button("Get Job Recommendations"):
    if sum(user_input) == 0:
        st.warning("Please select at least one skill!")
    else:
        distances, indices = knn.kneighbors([user_input])
        st.success("✅ Recommended Jobs:")
        for i in indices[0]:
            st.write("-", job_titles.iloc[i])
