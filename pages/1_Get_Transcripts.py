import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import snowflake.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_mock_data():
    """Generate mock transcript data for testing"""
    data = {
        'bot_name': ['SupportBot', 'SupportBot', 'SupportBot', 'SalesBot', 'SalesBot'],
        'conversation_id': ['conv1', 'conv1', 'conv2', 'conv3', 'conv3'],
        'mid': ['m1', 'm2', 'm3', 'm4', 'm5'],
        'utterance': [
            'How can I help you?',
            'I need help with my order',
            'What seems to be the problem?',
            'Hello, I want to buy a product',
            'Which product are you interested in?'
        ],
        'response': [
            'I can help you with that.',
            'Could you provide your order number?',
            'I understand. Let me check that for you.',
            'Welcome! I can help you with your purchase.',
            'We have several products available.'
        ],
        'datetime': [
            datetime.now() - timedelta(hours=2),
            datetime.now() - timedelta(hours=1, minutes=55),
            datetime.now() - timedelta(hours=1, minutes=50),
            datetime.now() - timedelta(hours=1),
            datetime.now() - timedelta(minutes=55)
        ]
    }
    return pd.DataFrame(data)

def connect_to_snowflake():
    """Establish connection to Snowflake"""
    try:
        conn = snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {str(e)}")
        return None

def get_transcripts_from_snowflake(bot_name, start_date, end_date):
    """Fetch transcripts from Snowflake"""
    conn = connect_to_snowflake()
    if conn:
        try:
            query = f"""
            SELECT bot_name, conversation_id, mid, utterance, response, datetime
            FROM transcripts
            WHERE bot_name = '{bot_name}'
            AND datetime BETWEEN '{start_date}' AND '{end_date}'
            ORDER BY conversation_id, datetime
            """
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            return None
    return None

st.title("Get Transcripts from Snowflake")

# Bot name input
bot_name = st.text_input("Enter Bot Name", "SupportBot")

# Date range selection
date_range = st.radio(
    "Select Date Range",
    ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Custom Range"]
)

if date_range == "Custom Range":
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")
else:
    end_date = datetime.now()
    if date_range == "Last 24 Hours":
        start_date = end_date - timedelta(days=1)
    elif date_range == "Last 7 Days":
        start_date = end_date - timedelta(days=7)
    else:  # Last 30 Days
        start_date = end_date - timedelta(days=30)

# Fetch data button
if st.button("Fetch Transcripts"):
    with st.spinner("Fetching transcripts..."):
        # For demo purposes, use mock data
        df = get_mock_data()
        if df is not None:
            st.session_state.transcripts_df = df
            st.success(f"Successfully loaded {len(df)} transcripts!")
            st.dataframe(df)
        else:
            st.error("Failed to fetch transcripts")

# Display current data if available
if st.session_state.transcripts_df is not None:
    st.subheader("Current Transcripts")
    st.dataframe(st.session_state.transcripts_df) 