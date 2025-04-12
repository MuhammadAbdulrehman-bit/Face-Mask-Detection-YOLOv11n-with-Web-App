import streamlit as st
import pandas as pd
import os
from PIL import Image
import datetime

st.title("Mask Violation Dashboard")

if os.path.exists("violations_log.csv"):
    df = pd.read_csv("violations_log.csv")
    st.dataframe(df)

    st.subheader("Search Violation Images by Timestamp")
    timestamp = st.text_input("Enter Timestamp(YYYY-MM-DD HH:MM:SS)", placeholder="2023-10-01 12:00:00")

    if timestamp:
        try:
            date = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") 
            file_name = f"violation_{date.strftime('%Y%m%d_%H%M%S')}"
            file_path = os.path.join("violations", file_name + ".jpg")
            print(file_path)

            if os.path.exists(file_path):
                st.image(Image.open(file_path), caption="Violation image at " + timestamp, width=500)
            else:
                st.error("No violation image found for this timestamp")
            

        except ValueError:
            st.error("Invalid timestamp format. Please use YYYY-MM-DD HH:MM:SS")
else:
    st.error("No violation log found. Please run the detection script first.")