import pytest
import pandas as pd
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv()

# Sample test data
@pytest.fixture
def sample_transcripts():
    return pd.DataFrame({
        'bot_name': ['SupportBot', 'SupportBot', 'SalesBot'],
        'conversation_id': ['conv1', 'conv1', 'conv2'],
        'mid': ['m1', 'm2', 'm3'],
        'utterance': [
            'How can I help you?',
            'I need help with my order',
            'Hello, I want to buy a product'
        ],
        'response': [
            'I can help you with that.',
            'Could you provide your order number?',
            'Welcome! I can help you with your purchase.'
        ],
        'datetime': [
            datetime.now() - timedelta(hours=2),
            datetime.now() - timedelta(hours=1, minutes=55),
            datetime.now() - timedelta(hours=1)
        ]
    })

@pytest.fixture
def sample_scores():
    return pd.DataFrame({
        'conversation_id': ['conv1', 'conv2'],
        'bot_name': ['SupportBot', 'SalesBot'],
        'datetime': [datetime.now() - timedelta(hours=2), datetime.now() - timedelta(hours=1)],
        'summary': ['Customer needed help with order', 'Customer wanted to buy a product'],
        'satisfaction_score': [4, 5],
        'accuracy_score': [4, 5],
        'relevancy_score': [4, 5],
        'containment_score': [4, 5]
    })

def test_transcript_format(sample_transcripts):
    """Test if transcript data has the correct format"""
    required_columns = ['bot_name', 'conversation_id', 'mid', 'utterance', 'response', 'datetime']
    assert all(col in sample_transcripts.columns for col in required_columns)
    assert len(sample_transcripts) > 0

def test_score_format(sample_scores):
    """Test if score data has the correct format"""
    required_columns = [
        'conversation_id', 'bot_name', 'datetime', 'summary',
        'satisfaction_score', 'accuracy_score', 'relevancy_score', 'containment_score'
    ]
    assert all(col in sample_scores.columns for col in required_columns)
    assert len(sample_scores) > 0

def test_score_ranges(sample_scores):
    """Test if scores are within valid ranges"""
    score_columns = ['satisfaction_score', 'accuracy_score', 'relevancy_score', 'containment_score']
    for col in score_columns:
        assert sample_scores[col].min() >= 1
        assert sample_scores[col].max() <= 5

def test_aws_credentials():
    """Test if AWS credentials are available"""
    assert os.getenv('AWS_ACCESS_KEY_ID') is not None
    assert os.getenv('AWS_SECRET_ACCESS_KEY') is not None
    assert os.getenv('AWS_REGION') is not None

def test_snowflake_credentials():
    """Test if Snowflake credentials are available (optional)"""
    # These tests will be skipped if Snowflake credentials are not provided
    if os.getenv('SNOWFLAKE_USER') is None:
        pytest.skip("Snowflake credentials not provided")
    assert os.getenv('SNOWFLAKE_PASSWORD') is not None
    assert os.getenv('SNOWFLAKE_ACCOUNT') is not None
    assert os.getenv('SNOWFLAKE_WAREHOUSE') is not None
    assert os.getenv('SNOWFLAKE_DATABASE') is not None
    assert os.getenv('SNOWFLAKE_SCHEMA') is not None

def test_json_export(sample_scores, tmp_path):
    """Test JSON export functionality"""
    # Create a temporary file
    temp_file = tmp_path / "test_scores.json"
    
    # Export scores to JSON
    json_data = sample_scores.to_json(orient='records', date_format='iso')
    temp_file.write_text(json_data)
    
    # Read back and verify
    loaded_data = pd.read_json(temp_file)
    assert len(loaded_data) == len(sample_scores)
    assert all(col in loaded_data.columns for col in sample_scores.columns)

def test_conversation_grouping(sample_transcripts):
    """Test conversation grouping functionality"""
    grouped = sample_transcripts.groupby('conversation_id').agg({
        'utterance': lambda x: '\n'.join(x),
        'response': lambda x: '\n'.join(x),
        'bot_name': 'first',
        'datetime': 'first'
    }).reset_index()
    
    assert len(grouped) == 2  # Should have 2 unique conversations
    assert 'conv1' in grouped['conversation_id'].values
    assert 'conv2' in grouped['conversation_id'].values 