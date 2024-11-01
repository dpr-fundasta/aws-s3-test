import streamlit as st
import requests
import base64

# Define the API endpoint URL
API_URL = "https://j0kn8pau5l.execute-api.ap-northeast-1.amazonaws.com/develop/upload"  

# Streamlit app
st.title("PDF Uploader to S3 via API")

# File uploader widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Display file size limit
st.write("Maximum file size: 10 MB")

if uploaded_file:
    # Check file size
    file_size = uploaded_file.size
    max_size = 10 * 1024 * 1024  # 10 MB in bytes
    
    if file_size > max_size:
        st.error("File exceeds the 10 MB limit. Please choose a smaller file.")
    else:
        # Read and encode the PDF file content in base64
        file_content = uploaded_file.read()
        file_content_base64 = base64.b64encode(file_content).decode("utf-8")
        
        # Get the file name
        file_name = uploaded_file.name
        
        # Prepare the JSON payload
        payload = {
            "file_name": file_name,
            "file_content": file_content_base64
        }
        
        # Send the POST request to the API
        with st.spinner("Uploading file..."):
            try:
                response = requests.post(API_URL, json=payload)
            except requests.RequestException as e:
                response = None
                st.error(f"Request failed: {e}")
        
        # Check the response if it's defined
        if response and response.status_code == 200:
            st.success("File uploaded successfully!")
        elif response:
            st.error(f"Failed to upload file. Status code: {response.status_code}")
            st.write(response.text)
        else:
            st.error("An error occurred while making the request.")
