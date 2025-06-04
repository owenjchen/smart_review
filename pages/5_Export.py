import streamlit as st
import pandas as pd
import boto3
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.title("Export Results")

def get_s3_client():
    """Initialize AWS S3 client"""
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        return s3
    except Exception as e:
        st.error(f"Error connecting to AWS S3: {str(e)}")
        return None

def export_to_s3(data, bucket_name, file_name):
    """Export data to S3 bucket"""
    s3 = get_s3_client()
    if s3 is None:
        return False
    
    try:
        # Convert DataFrame to JSON
        json_data = data.to_json(orient='records', date_format='iso')
        
        # Upload to S3
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json_data,
            ContentType='application/json'
        )
        return True
    except Exception as e:
        st.error(f"Error exporting to S3: {str(e)}")
        return False

if st.session_state.scores_df is not None:
    st.subheader("Export Scores to S3")
    
    # S3 bucket configuration
    bucket_name = st.text_input("S3 Bucket Name", os.getenv('AWS_S3_BUCKET', ''))
    
    # Generate default file name
    default_file_name = f"conversation_scores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    file_name = st.text_input("File Name", default_file_name)
    
    if st.button("Export to S3"):
        if not bucket_name:
            st.error("Please enter an S3 bucket name")
        else:
            with st.spinner("Exporting to S3..."):
                if export_to_s3(st.session_state.scores_df, bucket_name, file_name):
                    st.success(f"Successfully exported scores to s3://{bucket_name}/{file_name}")
                    
                    # Display S3 URL
                    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
                    st.markdown(f"**S3 URL:** [{s3_url}]({s3_url})")
    
    # Preview data to be exported
    st.subheader("Preview Data to Export")
    st.dataframe(st.session_state.scores_df)
    
else:
    st.warning("No scores available. Please process transcripts first using the Score Transcripts page.") 