import streamlit as st
import boto3
import uuid  # For unique file names
from botocore.exceptions import NoCredentialsError, ClientError
import json

# AWS configuration
AWS_ACCESS_KEY = st.secrets["AWS_ACCESS_KEY"]  # "your-access-key-id"
AWS_SECRET_KEY = st.secrets["AWS_SECRET_KEY"]  # "your-secret-access-key"
AWS_SESSION_TOKEN = str(IQoJb3JpZ2luX2VjEAwaDmFwLW5vcnRoZWFzdC0xIkcwRQIgCxJr+dbhs6xEY6l6NPUTBfJdbIAGIjpd4yHPn+k30EICIQCX1uJLdNTdDhSlrLIKA38KwEuAscWC91WSrgqRlGof/Sr4AQiF//////////8BEAQaDDI5NDkyMzQ4NDA1NiIMRuOzrtW8gvwjkXzHKswBUa3FsiheiKUwsLaqWLKxAvcyhsMopdcK9LRB+t6SXADV5UYdHchb4v9TFD+SjiUzxE9yzYvSgMnepAOCArFlL8Lgchu31C6YrmeEAyEi1laoN1BuiS8uD6Q0pNiC7Jc/xHXxPsAwaq6iDwjsNjZVQxBy+uqHV4GEPNtoKdqdZZ7SgLHGGLyHdX+Zfss+q5kIWUED81cW1dnHhOTesKkkFLLJ7AFJajd/SPuzxoa3W8Ot4WrngFDBoVpCHY5o1nzoOWa7FBfhwrS+6BPTMP+BjLkGOpgBC5jJ1n9v1UkVALpg4gtUtgyMoLqEjFF3cZWJvxZKqhB73vgnJoGh7CLMDaHARlImMgEyncU4qF8gouQR2WKtz+WX0Ekls7cwoWsNCAM2z4hdBEmDK377n3Q2oTj2GhpbEejl//p1C6eFphk1If9ClWs4oslZ7ybVikkjPycbYEx7m/avY/CsS9j4DJFPMmR9KgKns5fmYX0=) #st.secrets["AWS_SESSION_TOKEN"]  # "your-session-token"
AWS_REGION = st.secrets["AWS_REGION"]  # "your-region"
S3_BUCKET = st.secrets["S3_BUCKET"]

# Initialize S3 client with session token
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
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

# Streamlit UI
st.sidebar.title("FundastA R.A.G Chatbot")

uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    if st.sidebar.button("Upload and Trigger Lambda"):
        # Upload the PDF to S3
        s3_url = upload_pdf_to_s3(uploaded_file)

        if s3_url:
            st.sidebar.success(f"PDF uploaded to: {s3_url}")
