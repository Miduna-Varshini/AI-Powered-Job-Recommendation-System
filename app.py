# app.py

import streamlit as st
import pandas as pd
import joblib
import os

# ------------------------------
# File paths
# ------------------------------
MODEL_FILE = "knn_job_recommender.joblib"
SKILLS_FILE = "skills_list.joblib"
DATASET_FILE = "DataScientist.csv"

# ------------------------------
# Check files exist
# ------------------------------
for file in [MODEL_FILE, SKILLS_FILE, DATASET_FILE]:
    if not os.path.exists(file):
        st.error(f"❌ File not found: {file}. Make sure it's in the same folder as app.py")
        st.stop()

# ------------------------------
# Load KNN model and skills
# ------------------------------
knn = joblib.load(MODEL_FILE)
skills = joblib.load(SKILLS_FILE)

# ------------------------------
# Load job titles
# ------------------------------
df = pd.read_csv(DATASET_FILE)
# Clean column names
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

        # Optional: show distances
        st.write("\n📊 Distances to jobs:")
        for idx, dist in zip(indices[0], distances[0]):
            st.write(f"{job_titles.iloc[idx]} → Distance: {round(dist, 2)}")
