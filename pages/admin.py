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

# Display current scores and provide options to edit or delete
st.header("Current Scores")
if data['scores']:
    df = pd.DataFrame(data['scores'])
    df = df.sort_values(by='score', ascending=False).reset_index(drop=True)
    st.dataframe(df)

    # Provide edit and delete options
    for idx, row in df.iterrows():
        st.subheader(f"Edit Score for {row['name']} ({row['score']})")
        new_name = st.text_input(f"New Name for {row['name']}", value=row['name'], key=f"name_{idx}")
        new_score = st.number_input(f"New Score for {row['name']}", min_value=0.0, max_value=100.0, value=row['score'], step=0.1, key=f"score_{idx}")

        if st.button(f"Update {row['name']}", key=f"update_{idx}"):
            data['scores'][idx]['name'] = new_name
            data['scores'][idx]['score'] = new_score
            save_data(data)
            st.success(f"Updated {new_name} with score {new_score}")

        if st.button(f"Delete {row['name']}", key=f"delete_{idx}"):
            data['scores'].pop(idx)
            save_data(data)
            st.success(f"Deleted {row['name']}")
            st.experimental_rerun()

# Option to clear all scores
if st.button("Clear All Scores"):
    data['scores'] = []
    save_data(data)
    st.success("Cleared all scores")
