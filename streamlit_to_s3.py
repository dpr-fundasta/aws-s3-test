import os
import streamlit as st
import boto3

# Fetch AWS credentials from environment variables
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Initialize the S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# Define the bucket name
BUCKET_NAME = "fileupload-deepu"

def list_buckets():
    # Fetch the list of buckets from S3
    buckets_resp = s3.list_buckets()
    return [bucket['Name'] for bucket in buckets_resp['Buckets']]

# Streamlit app
st.title("S3 Bucket List")

# Button to retrieve and display buckets
if st.button("List Buckets"):
    buckets = list_buckets()
    if buckets:
        st.write("Available Buckets:")
        for bucket in buckets:
            st.write(f"- {bucket}")
    else:
        st.write("No buckets found.")
