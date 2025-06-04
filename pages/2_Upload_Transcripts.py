import streamlit as st
import pandas as pd
import json

st.title("Upload Transcripts")

def load_csv(file):
    """Load CSV file into pandas DataFrame"""
    try:
        df = pd.read_csv(file)
        required_columns = ['bot_name', 'conversation_id', 'mid', 'utterance', 'response', 'datetime']
        if not all(col in df.columns for col in required_columns):
            st.error("CSV file must contain all required columns: bot_name, conversation_id, mid, utterance, response, datetime")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {str(e)}")
        return None

def load_json(file):
    """Load JSON file into pandas DataFrame"""
    try:
        data = json.load(file)
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            st.error("JSON file must contain a list of transcript objects")
            return None
        
        required_columns = ['bot_name', 'conversation_id', 'mid', 'utterance', 'response', 'datetime']
        if not all(col in df.columns for col in required_columns):
            st.error("JSON file must contain all required columns: bot_name, conversation_id, mid, utterance, response, datetime")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading JSON file: {str(e)}")
        return None

# File upload section
st.subheader("Upload Transcript File")
uploaded_file = st.file_uploader("Choose a file", type=['csv', 'json'])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = load_csv(uploaded_file)
    else:  # JSON file
        df = load_json(uploaded_file)
    
    if df is not None:
        st.session_state.transcripts_df = df
        st.success(f"Successfully loaded {len(df)} transcripts!")
        st.dataframe(df)

# Display current data if available
if st.session_state.transcripts_df is not None:
    st.subheader("Current Transcripts")
    st.dataframe(st.session_state.transcripts_df) 