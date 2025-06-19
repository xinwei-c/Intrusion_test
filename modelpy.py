#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import section
import streamlit as st
import pandas as pd
from datetime import datetime


# In[ ]:


# #clean
# df = pd.read_csv("word_intrusion.csv")
# df['Words_with_Intruder_Shuffled'] = df['Words_with_Intruder_Shuffled'].apply(eval)
# df = df.drop_duplicates(subset=['Topic_ID'])  # One question per topic

# #start set
# if 'started' not in st.session_state:
#     st.session_state.started = False
# if 'current_index' not in st.session_state:
#     st.session_state.current_index = 0
# if 'responses' not in st.session_state:
#     st.session_state.responses = []

# #instruction 
# if not st.session_state.started:
#     st.title("Word Intrusion Evaluation")
#     st.markdown("""
#     Thank you for participating in this short evaluation task.

#     In this task, you will see a group of words. One of the words **does not belong** to the group.
    
#     Your job is to choose the word that is least related to the others.

#     **Consent**: By clicking “Start,” you agree to let us anonymously store your responses for academic purposes. Your answers will be used for topic model evaluation. No personal information is collected.
#     """)

#     if st.button("✅ Start"):
#         st.session_state.started = True
#     st.stop()

# #end
# if st.session_state.current_index >= len(df):
#     st.title("🎉 Thank you for your participation!")
#     st.write("You've completed all the questions. Your results are saved.")

#     result_df = pd.DataFrame(st.session_state.responses)
#     result_df['is_correct'] = result_df['selected'] == result_df['correct']
#     result_df['accuracy'] = result_df['is_correct'].astype(int)

#     csv = result_df.to_csv(index=False).encode('utf-8')
#     st.download_button("📥 Researcher: Download Results CSV", csv, "intrusion_results.csv", "text/csv")
#     st.stop()

# # --- Display current task ---
# row = df.iloc[st.session_state.current_index]
# topic_name = row['Topic_Name']
# words = row['Words_with_Intruder_Shuffled']
# correct_word = row['Intruder']

# st.title("🔍 Word Intrusion Task")
# st.subheader(f"Topic: {topic_name}")
# user_choice = st.radio("Which word does NOT belong?", options=words)

# # --- Submit logic ---
# if st.button("Submit"):
#     st.session_state.responses.append({
#         "timestamp": datetime.now().isoformat(),
#         "topic_id": row['Topic_ID'],
#         "topic_name": topic_name,
#         "words": words,
#         "selected": user_choice,
#         "correct": correct_word,
#     })
#     st.session_state.current_index += 1
#     st.rerun()


# In[ ]:


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
    st.write("You’ve completed all the questions.")

    # Save response to downloadable CSV
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
#user_choice = st.radio("", options=words)

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

