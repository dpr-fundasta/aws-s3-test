# streamlit_app.py

import streamlit as st
import requests

# Lambda function URL
LAMBDA_API_URL = "https://zxjhrr7n44.execute-api.ap-northeast-1.amazonaws.com/generates3url"

st.title("Upload PDF to S3")

# Step 1: File Upload Selection
pdf_file = st.file_uploader("Choose a PDF file to upload", type="pdf")

if pdf_file is not None:
    if st.button("Upload"):
        # Step 2: Request Presigned URL from AWS Lambda
        response = requests.post(LAMBDA_API_URL, json={"filename": pdf_file.name})
        
        if response.status_code == 200:
            # Extract presigned URL from the Lambda response
            presigned_url = response.json().get("presigned_url")
            
            # Step 3: Upload File to S3 using the Presigned URL
            files = {"file": (pdf_file.name, pdf_file, "application/pdf")}
            
            # We use PUT here to match the presigned URL's expected method
            upload_response = requests.put(presigned_url, data=pdf_file.getvalue(), headers={"Content-Type": "application/pdf"})
            
            if upload_response.status_code == 200:
                st.success("File uploaded successfully to S3!")
            else:
                st.error("Failed to upload file to S3. Status code: " + str(upload_response.status_code))
        else:
            st.error("Failed to get presigned URL from Lambda.")
