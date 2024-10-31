import streamlit as st
import requests

# Define the URL for the AWS API Gateway
api_gateway_url = "https://zxjhrr7n44.execute-api.ap-northeast-1.amazonaws.com/generates3url"

st.title("PDF Upload to AWS")

# File uploader widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Upload button
if uploaded_file is not None and st.button("Upload PDF"):
    # Convert the uploaded file to bytes
    file_bytes = uploaded_file.read()
    files = {"file": (uploaded_file.name, file_bytes, "application/pdf")}

    # Send PDF to API Gateway endpoint
    response = requests.post(api_gateway_url, files=files)

    # Display success message based on Lambda's response
    if response.status_code == 200:
        st.success("PDF uploaded successfully.")
    else:
        st.error("Failed to upload PDF.")
