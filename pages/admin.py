import streamlit as st
import pandas as pd
import json

# File path to store data
DATA_FILE = 'leaderboard_data.json'

# Load data from JSON file
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {'main_title': "Mr. Ward's Leaderboard", 'title': "Top 5 Scores", 'scores': []}
    return data

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Initialize the data
data = load_data()

st.title("Admin Page - Update Scores")

# Section to change the main title
st.header("Update Main Title")
new_main_title = st.text_input("Main Title", data['main_title'])
if st.button("Update Main Title"):
    data['main_title'] = new_main_title
    save_data(data)
    st.success(f"Updated main title to: {new_main_title}")

# Section to change the subtitle (optional, if needed)
# st.header("Update Leaderboard Title")
# new_title = st.text_input("Leaderboard Title", data['title'])
# if st.button("Update Title"):
#     data['title'] = new_title
#     save_data(data)
#     st.success(f"Updated title to: {new_title}")

st.header("Enter New Score")
name = st.text_input("Student Name")
score = st.number_input("Score", min_value=0.0, max_value=100.0, step=0.1, format="%.1f")

if st.button("Add Score"):
    if name and score is not None:
        data['scores'].append({'name': name, 'score': round(score, 1)})
        save_data(data)
        st.success(f"Added {name} with score {score}")
    else:
        st.error("Please enter both name and score")

# Option to clear scores
if st.button("Clear All Scores"):
    data['scores'] = []
    save_data(data)
    st.success("Cleared all scores")
