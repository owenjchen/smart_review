import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.title("Dashboard")

def create_histogram(df, column, title):
    """Create a histogram with mean line"""
    fig = px.histogram(
        df,
        x=column,
        nbins=5,
        title=title,
        labels={column: "Score"},
        range_x=[0, 6]
    )
    
    # Add mean line
    mean_value = df[column].mean()
    fig.add_vline(
        x=mean_value,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean: {mean_value:.2f}",
        annotation_position="top right"
    )
    
    return fig

if st.session_state.scores_df is not None:
    df = st.session_state.scores_df
    
    # Display overall statistics
    st.subheader("Overall Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Conversations", len(df))
    with col2:
        st.metric("Unique Bots", df['bot_name'].nunique())
    with col3:
        st.metric("Average Satisfaction", f"{df['satisfaction_score'].mean():.2f}")
    with col4:
        st.metric("Average Accuracy", f"{df['accuracy_score'].mean():.2f}")
    
    # Create histograms for each metric
    st.subheader("Score Distributions")
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_histogram(df, 'satisfaction_score', 'Satisfaction Score Distribution'), use_container_width=True)
        st.plotly_chart(create_histogram(df, 'accuracy_score', 'Accuracy Score Distribution'), use_container_width=True)
    with col2:
        st.plotly_chart(create_histogram(df, 'relevancy_score', 'Relevancy Score Distribution'), use_container_width=True)
        st.plotly_chart(create_histogram(df, 'containment_score', 'Containment Score Distribution'), use_container_width=True)
    
    # Correlation heatmap
    st.subheader("Score Correlations")
    correlation_matrix = df[['satisfaction_score', 'accuracy_score', 'relevancy_score', 'containment_score']].corr()
    fig = px.imshow(
        correlation_matrix,
        labels=dict(color="Correlation"),
        title="Score Correlation Matrix"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Time series of scores
    st.subheader("Score Trends Over Time")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime')
    
    fig = go.Figure()
    for score in ['satisfaction_score', 'accuracy_score', 'relevancy_score', 'containment_score']:
        fig.add_trace(go.Scatter(
            x=df['datetime'],
            y=df[score],
            name=score.replace('_', ' ').title(),
            mode='lines+markers'
        ))
    
    fig.update_layout(
        title="Score Trends Over Time",
        xaxis_title="Date",
        yaxis_title="Score",
        yaxis_range=[0, 6]
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Bot comparison
    st.subheader("Bot Performance Comparison")
    bot_stats = df.groupby('bot_name')[['satisfaction_score', 'accuracy_score', 'relevancy_score', 'containment_score']].mean()
    
    fig = go.Figure()
    for score in ['satisfaction_score', 'accuracy_score', 'relevancy_score', 'containment_score']:
        fig.add_trace(go.Bar(
            name=score.replace('_', ' ').title(),
            x=bot_stats.index,
            y=bot_stats[score]
        ))
    
    fig.update_layout(
        title="Average Scores by Bot",
        xaxis_title="Bot Name",
        yaxis_title="Score",
        yaxis_range=[0, 6],
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.warning("No scores available. Please process transcripts first using the Score Transcripts page.") 