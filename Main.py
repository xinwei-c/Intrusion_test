#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import section
import streamlit as st
import pandas as pd
from datetime import datetime

#import gspread
#from google.oauth2.service_account import Credentials

#scope = ["https://www.googleapis.com/auth/spreadsheets"]
    
st.set_page_config(page_title="Intrusion Evaluation", layout="centered")

st.sidebar.title("🔧 Select Task")
task = st.sidebar.radio("Choose a task to evaluate:", ["Word Intrusion", "Document Intrusion"])

if task == "Word Intrusion":
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

        result_df = pd.DataFrame(st.session_state.responses)
        result_df['is_correct'] = result_df['selected'] == result_df['correct']
        result_df['accuracy'] = result_df['is_correct'].astype(int)

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



# add docs
elif task == "Document Intrusion":
    #load csv
    @st.cache_data
    def load_data():
        df = pd.read_csv("document_intrusion.csv")
        df['Docss_with_Intruder_Shuffled'] = df['Docs_with_Intruder_Shuffled'].apply(eval)
        return df.drop_duplicates(subset=['Topic_ID'])

    df = load_data()

    # Session setup
    if 'started' not in st.session_state:
        st.session_state.started = False
    if 'participant_id' not in st.session_state:
        st.session_state.participant_id = ""
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'responses' not in st.session_state:
        st.session_state.responses = []

    # Consent & ID
    if not st.session_state.started:
        st.title("📄 Document Intrusion Evaluation")
        st.markdown("""
        Welcome! In this task, you’ll see several Reddit posts. One post does **not** belong with the rest.

        Your job is to pick the **intruder** post.

        **By clicking Start, you consent to participate.** Your answers will be collected anonymously.
        """)
        st.session_state.participant_id = st.text_input("Enter your Participant ID to begin:")
        if st.session_state.participant_id and st.button("✅ Start"):
            st.session_state.started = True
        st.stop()

    # End of questions
    if st.session_state.current_index >= len(df):
        st.title("🎉 Thank you!")
        st.write("You've completed all document intrusion questions.")

        result_df = pd.DataFrame(st.session_state.responses)
        result_df['is_correct'] = result_df['selected'] == result_df['correct']
        result_df['accuracy'] = result_df['is_correct'].astype(int)

        csv = result_df.to_csv(index=False).encode('utf-8')
        filename = f"doc_results_{st.session_state.participant_id}.csv"
        st.download_button("Download Your Results", csv, filename, mime='text/csv')
        st.stop()

    # Current document intrusion question
    row = df.iloc[st.session_state.current_index]
    topic_name = row['Topic_Name']
    docs = row['Documents_with_Intruder_Shuffled']
    correct_doc = row['Intruder']

    st.title("🔍 Document Intrusion Task")
    st.subheader("Which document does NOT belong?")
    user_choice = st.radio("Select the intruder document:", options=docs)

    if st.button("Submit"):
        st.session_state.responses.append({
            "timestamp": datetime.now().isoformat(),
            "participant_id": st.session_state.participant_id,
            "topic_id": row['Topic_ID'],
            "topic_name": topic_name,
            "documents": docs,
            "selected": user_choice,
            "correct": correct_doc,
        })
        st.session_state.current_index += 1
        st.rerun()
