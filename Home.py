import streamlit as st

st.set_page_config(
    page_title="Smart Review",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Smart Review")
st.subheader("AI-Powered Conversation Transcript Analysis")

st.markdown("""
Welcome to Smart Review! This application helps you analyze and evaluate conversation transcripts using AI.

### Features:
1. **Get Transcripts**: Import conversation transcripts from Snowflake
2. **Upload Transcripts**: Upload local transcript files (CSV/JSON)
3. **Score Transcripts**: Analyze conversations using AI
4. **Dashboard**: View detailed analytics and metrics
5. **Export**: Save results to AWS S3

### Getting Started:
Select a feature from the sidebar to begin analyzing your conversation transcripts.
""")

# Initialize session state variables if they don't exist
if 'transcripts_df' not in st.session_state:
    st.session_state.transcripts_df = None
if 'scores_df' not in st.session_state:
    st.session_state.scores_df = None 