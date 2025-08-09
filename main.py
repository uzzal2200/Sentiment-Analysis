import streamlit as st
import pandas as pd
import requests
from io import BytesIO

prediction_endpoint = "http://127.0.0.1:5000/predict"

st.title("Text Sentiment Predictor")

uploaded_file = st.file_uploader(
    "Choose a CSV file for bulk prediction - Upload the file and click on Predict",
    type="csv",
)

user_input = st.text_input("Enter text and click on Predict", "")

if st.button("Predict"):
    if uploaded_file is not None:
        file = {"file": uploaded_file}
        response = requests.post(prediction_endpoint, files=file)
        if response.status_code == 200:
            response_bytes = BytesIO(response.content)
            response_df = pd.read_csv(response_bytes)
            st.download_button(
                label="Download Predictions",
                data=response_bytes,
                file_name="Predictions.csv",
                key="result_download_button",
            )
        else:
            st.error("Error in prediction request.")
    else:
        # ✅ JSON আকারে টেক্সট পাঠানো
        response = requests.post(prediction_endpoint, json={"text": user_input})
        if response.status_code == 200:
            response = response.json()
            st.write(f"Predicted sentiment: {response['prediction']}")
        else:
            st.error("Error in prediction request.")

