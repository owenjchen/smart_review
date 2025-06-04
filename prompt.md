Create a Python web app based called Smart Review that is an AI-powered application to use an LLM as a judge to review conversation transcripts.  Use Streamlit to create Smart Review as a multipage app.

(1) Get Transcripts from Snowflake:
Ingest conversation transcripts from a Snowflake database based on filters of bot name, start date time, end date time.  Prompt user enter bot name, and date ranges (last 24 hours, last 7 days, last 30 days or a custom start and end date range). Once user selects the parameters, connect to Snowflak database and pull data into memory.  Store the results in a pandas dataframe.  The transcript table contains these columns: bot name, conversion_id, mid, utterance, response, datetime.
Use a mockup transcript data to display in the initial UI.

(2) Upload Transcripts:
As an alternative to get transcripts from Snowflake, offer a local file upload functionality.  Let user browse a local file in csv or json format.  Upload it to memory and store in a pandas dataframe.

(3) Score Transcripts:
Process each conversation transcript identified by conservation id using an LLM such as Anthropic Cluade 4 through Amazon Bedrock runtime. Ask Anthropic Claude 4 to perform the following tasks for each conversation: a) summarize the conversation; b) generate a satisfaction score on a scale of 1-5; (c) generate a score of accuracy on a scale of 1-5 on the bot responses;(d) generate a score of relevancy on a scale of 1-5 on the bot responses; (e) generate a score of containment on a scale of 1-5 whether the user issue being resolved.
Store conversation scores in a pandas dataframe along with the transcripts.  Display a run time information and mean values of all metrics.

(4) Dashboard
Create a dashboard to display conversation scores.  Plot a histogram on each metric with a horizon bar showing a mean value. 

(5) Export
Export the conversation scores to a json file on an S3 bucket on AWS.

Ignore user login.  Make it a public app.
Create a working Python app code based on Streamlit.
Create a requirements file with dependencies of Snowflake, AWS Bedrock, and S3
Generate test cases
