import streamlit as st
import boto3
import uuid  # For unique file names
from botocore.exceptions import NoCredentialsError, ClientError

# AWS configuration
AWS_ACCESS_KEY = st.secrets["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = st.secrets["AWS_SECRET_KEY"]
AWS_REGION = st.secrets["AWS_REGION"]
S3_BUCKET = st.secrets["S3_BUCKET"]

# Initialize S3 and DynamoDB clients
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

dynamodb_client = boto3.client(
    'dynamodb',
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

def list_bucket_contents():
    """List the contents of the S3 bucket."""
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
        if 'Contents' in response:
            files = [item['Key'] for item in response['Contents']]
            return files
        else:
            return []

    except ClientError as e:
        st.error(f"Failed to list bucket contents: {e.response['Error']['Message']}")
        return None

def list_dynamodb_tables():
    """List DynamoDB tables."""
    try:
        response = dynamodb_client.list_tables()
        tables = response.get("TableNames", [])
        return tables

    except ClientError as e:
        st.error(f"Failed to list DynamoDB tables: {e.response['Error']['Message']}")
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

# List bucket contents button
if st.sidebar.button("List Bucket Contents"):
    files = list_bucket_contents()
    if files:
        st.sidebar.write("Files in bucket:")
        for file in files:
            st.sidebar.write(file)
    else:
        st.sidebar.write("No files found in the bucket.")

# List DynamoDB tables button
if st.sidebar.button("List DynamoDB Tables"):
    tables = list_dynamodb_tables()
    if tables:
        st.sidebar.write("DynamoDB Tables:")
        for table in tables:
            st.sidebar.write(table)
    else:
        st.sidebar.write("No DynamoDB tables found.")
