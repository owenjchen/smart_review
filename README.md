# Smart Review

Smart Review is an AI-powered application that uses LLMs to analyze and evaluate conversation transcripts. The application provides insights into conversation quality through various metrics such as satisfaction, accuracy, relevancy, and containment scores.

## Features

1. **Get Transcripts**: Import conversation transcripts from Snowflake
2. **Upload Transcripts**: Upload local transcript files (CSV/JSON)
3. **Score Transcripts**: Analyze conversations using Amazon Bedrock's Claude model
4. **Dashboard**: View detailed analytics and metrics
5. **Export**: Save results to AWS S3

## Prerequisites

- Python 3.8 or higher
- AWS Account with Bedrock access
- Snowflake Account (optional)
- AWS S3 Bucket (optional)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smart_review.git
cd smart_review
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following variables:
```
# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
AWS_S3_BUCKET=your_s3_bucket_name

# Snowflake Configuration (optional)
SNOWFLAKE_USER=your_snowflake_user
SNOWFLAKE_PASSWORD=your_snowflake_password
SNOWFLAKE_ACCOUNT=your_snowflake_account
SNOWFLAKE_WAREHOUSE=your_snowflake_warehouse
SNOWFLAKE_DATABASE=your_snowflake_database
SNOWFLAKE_SCHEMA=your_snowflake_schema
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run Home.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. Follow the workflow:
   - Get transcripts from Snowflake or upload local files
   - Process transcripts to generate scores
   - View analytics in the dashboard
   - Export results to S3

## Data Format

The application expects transcript data in the following format:

### CSV/JSON Format
```json
{
    "bot_name": "string",
    "conversation_id": "string",
    "mid": "string",
    "utterance": "string",
    "response": "string",
    "datetime": "ISO datetime string"
}
```

## Testing

Run the test suite:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 