import streamlit as st
import pandas as pd
import boto3
import json
import time
from datetime import datetime

st.title("Score Transcripts")

def get_bedrock_client():
    """Initialize Amazon Bedrock client"""
    try:
        bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-1'  # Change this to your AWS region
        )
        return bedrock
    except Exception as e:
        st.error(f"Error connecting to Amazon Bedrock: {str(e)}")
        return None

def analyze_conversation(bedrock, conversation):
    """Analyze a single conversation using Claude"""
    prompt = f"""Please analyze the following conversation and provide:
1. A brief summary
2. A satisfaction score (1-5)
3. An accuracy score (1-5)
4. A relevancy score (1-5)
5. A containment score (1-5)

Conversation:
{conversation}

Please provide the analysis in JSON format with the following structure:
{{
    "summary": "brief summary here",
    "satisfaction_score": number,
    "accuracy_score": number,
    "relevancy_score": number,
    "containment_score": number
}}"""

    try:
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 1000,
                "temperature": 0.5,
            })
        )
        
        response_body = json.loads(response['body'].read())
        return json.loads(response_body['completion'])
    except Exception as e:
        st.error(f"Error analyzing conversation: {str(e)}")
        return None

def process_transcripts():
    """Process all transcripts and generate scores"""
    if st.session_state.transcripts_df is None:
        st.error("No transcripts available. Please load transcripts first.")
        return None

    bedrock = get_bedrock_client()
    if bedrock is None:
        return None

    # Group transcripts by conversation_id
    conversations = st.session_state.transcripts_df.groupby('conversation_id').agg({
        'utterance': lambda x: '\n'.join(x),
        'response': lambda x: '\n'.join(x),
        'bot_name': 'first',
        'datetime': 'first'
    }).reset_index()

    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, conv in conversations.iterrows():
        status_text.text(f"Processing conversation {idx + 1} of {len(conversations)}")
        
        conversation_text = f"Bot: {conv['bot_name']}\nUser: {conv['utterance']}\nBot: {conv['response']}"
        analysis = analyze_conversation(bedrock, conversation_text)
        
        if analysis:
            results.append({
                'conversation_id': conv['conversation_id'],
                'bot_name': conv['bot_name'],
                'datetime': conv['datetime'],
                'summary': analysis['summary'],
                'satisfaction_score': analysis['satisfaction_score'],
                'accuracy_score': analysis['accuracy_score'],
                'relevancy_score': analysis['relevancy_score'],
                'containment_score': analysis['containment_score']
            })
        
        progress_bar.progress((idx + 1) / len(conversations))
        time.sleep(0.1)  # Small delay to prevent rate limiting

    status_text.empty()
    progress_bar.empty()

    if results:
        scores_df = pd.DataFrame(results)
        st.session_state.scores_df = scores_df
        return scores_df
    return None

# Process transcripts button
if st.button("Process Transcripts"):
    if st.session_state.transcripts_df is not None:
        with st.spinner("Processing transcripts..."):
            scores_df = process_transcripts()
            if scores_df is not None:
                st.success("Successfully processed all transcripts!")
                st.dataframe(scores_df)
                
                # Display mean scores
                st.subheader("Mean Scores")
                mean_scores = scores_df[['satisfaction_score', 'accuracy_score', 
                                      'relevancy_score', 'containment_score']].mean()
                st.write(mean_scores)
    else:
        st.error("Please load transcripts first using either the Get Transcripts or Upload Transcripts page.")

# Display current scores if available
if st.session_state.scores_df is not None:
    st.subheader("Current Scores")
    st.dataframe(st.session_state.scores_df) 