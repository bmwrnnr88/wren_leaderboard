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

# Initialize the data
data = load_data()

# Custom CSS for larger fonts
st.markdown("""
    <style>
        .leaderboard-main-title {
            font-size: 40px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .leaderboard-subtitle {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .leaderboard-table th, .leaderboard-table td {
            font-size: 24px;
            padding: 8px;
        }
        .medal {
            font-size: 24px; /* Adjust the font size for medal icons */
        }
        .rank-number {
            font-size: 24px; /* Adjust the font size for rank numbers */
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f"<div class='leaderboard-main-title'>{data['main_title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='leaderboard-subtitle'>{data['title']}</div>", unsafe_allow_html=True)

df = pd.DataFrame(data['scores'])

if not df.empty:
    df = df.sort_values(by='score', ascending=False)
    top_scores = df['score'].unique()[:5]
    df = df[df['score'].isin(top_scores)]

    def get_rank_marker(idx):
        if idx == 0:
            return "<span class='medal'>🥇</span>"
        elif idx == 1:
            return "<span class='medal'>🥈</span>"
        elif idx == 2:
            return "<span class='medal'>🥉</span>"
        elif idx == 3:
            return "<span class='rank-number'>4</span>"
        elif idx == 4:
            return "<span class='rank-number'>5</span>"
        else:
            return ""

    grouped = df.groupby('score')['name'].apply(list).reset_index()
    grouped = grouped.sort_values(by='score', ascending=False).reset_index(drop=True)

    leaderboard_html = "<table class='leaderboard-table' style='width:100%; border-collapse: collapse;'>"
    leaderboard_html += "<tr><th style='text-align: left;'>Rank</th><th style='text-align: left;'>Names</th><th style='text-align: left;'>Score</th></tr>"
    
    for idx, row in grouped.iterrows():
        rank_marker = get_rank_marker(idx)
        color = "gold" if idx == 0 else "silver" if idx == 1 else "bronze" if idx == 2 else "white"
        names = ", ".join(row['name'])
        leaderboard_html += f"<tr style='background-color: {color};'><td>{rank_marker}</td><td>{names}</td><td>{row['score']:.1f}</td></tr>"
    
    leaderboard_html += "</table>"
    st.markdown(leaderboard_html, unsafe_allow_html=True)
else:
    st.write("No scores available yet.")
