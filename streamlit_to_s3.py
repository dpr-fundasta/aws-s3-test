import streamlit as st
import boto3
import uuid  # For unique file names
from botocore.exceptions import NoCredentialsError, ClientError
import json

# AWS configuration
AWS_ACCESS_KEY = st.secrets["AWS_ACCESS_KEY"] #"your-access-key-id"
AWS_SECRET_KEY = st.secrets["AWS_SECRET_KEY"] #"your-secret-access-key"
AWS_REGION = st.secrets["AWS_REGION"]         #"your-region"
S3_BUCKET = st.secrets["S3_BUCKET"]
LAMBDA_FUNCTION_NAME = st.secrets["LAMBDA_FUNCTION_NAME"] #"your-lambda-function-name"

# Initialize S3 and Lambda clients
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)
def upload_pdf_to_s3(file):
    """Upload the PDF to S3 and return the S3 URL."""
    if file.size > 10 * 1024 * 1024:  # Example limit: 10 MB
        st.error("File size exceeds 10 MB limit.")
        return None
    
    try:
        unique_filename = f"{uuid.uuid4()}.pdf"
        s3_client.upload_fileobj(file, S3_BUCKET, unique_filename)
        s3_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{unique_filename}"
        return s3_url

    except NoCredentialsError:
        st.error("AWS credentials not available.")
        return None
    except ClientError as e:
        st.error(f"Failed to upload PDF: {e.response['Error']['Message']}")
        return None

def invoke_lambda(s3_url):
    """Invoke the Lambda function with the S3 URL as payload."""
    payload = {"s3_url": s3_url}
    try:
        response = lambda_client.invoke(
            FunctionName=LAMBDA_FUNCTION_NAME,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload),
        )
        response_payload = response['Payload'].read().decode('utf-8')
        if response['StatusCode'] == 200:
            return response_payload
        else:
            st.error(f"Error invoking Lambda function: {response['StatusCode']}")
            return None

    except ClientError as e:
        st.error(f"Failed to invoke Lambda function: {e.response['Error']['Message']}")
        return None

# Streamlit UI
st.sidebar.title("FundastA R.A.G Chatbot")

uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    if st.sidebar.button("Upload and Trigger Lambda"):
        # Upload the PDF to S3
        s3_url = upload_pdf_to_s3(uploaded_file)

        if s3_url:
            st.sidebar.success(f"PDF uploaded to: {s3_url}")
            
            # Invoke Lambda function
            response = invoke_lambda(s3_url)

            if response:
                st.sidebar.success(f"Upserting to Database. Response: {response}")
