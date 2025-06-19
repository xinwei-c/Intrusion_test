#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import section
import streamlit as st
import pandas as pd
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

def upload_to_google_sheet(data_dict):
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("gspread_creds.json", scopes=scope)
    client = gspread.authorize(creds)

    sheet = client.open("Surveyresults").sheet1 
    sheet.append_row(list(data_dict.values()))

#load csv
@st.cache_data
def load_data():
    df = pd.read_csv("word_intrusion.csv")
    df['Words_with_Intruder_Shuffled'] = df['Words_with_Intruder_Shuffled'].apply(eval)
    return df.drop_duplicates(subset=['Topic_ID'])

df = load_data()

#set
if 'started' not in st.session_state:
    st.session_state.started = False
if 'participant_id' not in st.session_state:
    st.session_state.participant_id = ""
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'responses' not in st.session_state:
    st.session_state.responses = []

#consent+id
if not st.session_state.started:
    st.title("🧠 Word Intrusion Evaluation")

    st.markdown("""
    Welcome! In this task, you'll see a group of words. One word does **not** belong.

    Your job is to identify that **intruder word**.

    **By clicking Start, you consent to participate.** Your answers will be collected anonymously.
    """)
    
    st.session_state.participant_id = st.text_input("Enter your Participant ID to begin:")

    if st.session_state.participant_id and st.button("✅ Start"):
        st.session_state.started = True
    st.stop()

#end

if st.session_state.current_index >= len(df):
    st.title("🎉 Thank you!")
    st.write("You've completed all questions.")

    # Create result DataFrame
    result_df = pd.DataFrame(st.session_state.responses)
    result_df['is_correct'] = result_df['selected'] == result_df['correct']
    result_df['accuracy'] = result_df['is_correct'].astype(int)

    # Upload each row to Google Sheets
    for row in result_df.to_dict(orient='records'):
        upload_to_google_sheet(row)

    # Optionally offer CSV download
    csv = result_df.to_csv(index=False).encode('utf-8')
    filename = f"results_{st.session_state.participant_id}.csv"
    st.download_button("📥 Download Your Results", csv, filename, mime='text/csv')

    st.stop()

#current question
row = df.iloc[st.session_state.current_index]
topic_name = row['Topic_Name']
words = row['Words_with_Intruder_Shuffled']
correct_word = row['Intruder']

st.title("🔍 Word Intrusion Task")
st.subheader(f"Which word does NOT belong?")
user_choice = st.radio("", options=words)

#submit
if st.button("Submit"):
    st.session_state.responses.append({
        "timestamp": datetime.now().isoformat(),
        "participant_id": st.session_state.participant_id,
        "topic_id": row['Topic_ID'],
        "topic_name": topic_name,
        "words": words,
        "selected": user_choice,
        "correct": correct_word,
    })
    st.session_state.current_index += 1
    st.rerun()
