# -*- coding: utf-8 -*-
"""app.py

This file hosts the front end of the demo for the full solution.

# Module 1 - DocIntelligence with OCR Tesseract libraries
"""

import os
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.saving import register_keras_serializable
import subprocess
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pytesseract
import tempfile
import fitz  # PyMuPDF for handling PDFs

# Set page configuration
st.set_page_config(
    page_title="Allnorth Consultants - RFO Central Application",
    layout="wide",
    page_icon="🧑‍⚕️"
)

# Placeholder model setup to replace GCN
working_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(working_dir, 'saved_models', 'doc_intelligence_model.keras')

if not os.path.exists(model_path):
    # Creating a simple placeholder model
    model = Sequential([
        Dense(64, activation='relu', input_shape=(100,)),  # Example input shape
        Dense(4, activation='softmax')  # Assuming 4 classes
    ])
    model.save(model_path)

doc_intelligence_model = tf.keras.models.load_model(model_path)

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        'Multiple AI Improvements - RFO Central Application',
        [
            'Doc Intelligence',
            "Predictive Analytics for Operational Planning",
            "Real-Time Fault Monitoring - Real Time Field Tech Assistance",
            "Project Completion Reporting for Oil and Gas"
        ],
        menu_icon='hospital-fill',
        icons=['activity', 'heart', 'person'],
        default_index=0
    )

# Doc Intelligence Page
if selected == 'Doc Intelligence':
    st.title('Doc Intelligence with CNNs and GCNs')

    # File uploader for multiple files
    uploaded_files = st.file_uploader("Upload your documents (images, PDFs)", type=['png', 'jpg', 'jpeg', 'pdf'], accept_multiple_files=True)

    # Function to upload file to Kaggle dataset
    def upload_to_kaggle(file_path, dataset_slug):
        try:
            subprocess.run(
                ["kaggle", "datasets", "upload", "-p", file_path, "--dir-mode", "zip", "-m", dataset_slug],
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    # Process each uploaded file
    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.write(f"Processing: {uploaded_file.name}")

            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            # Handle image files
            if uploaded_file.type.startswith("image/"):
                image = Image.open(temp_file_path)
                st.image(image, caption="Uploaded Image", use_column_width=True)

                if st.button("Extract Text from Image", key=uploaded_file.name):
                    extracted_text = pytesseract.image_to_string(image)
                    st.subheader("Extracted Text:")
                    st.write(extracted_text if extracted_text else "No text found.")

            # Handle PDF files
            elif uploaded_file.type == "application/pdf":
                doc_text = ""
                pdf = fitz.open(temp_file_path)
                for page_num in range(pdf.page_count):
                    page = pdf[page_num]
                    doc_text += page.get_text("text")
                st.subheader("Extracted Text from PDF:")
                st.write(doc_text if doc_text else "No text found in PDF.")
                pdf.close()

            # Uploading to Kaggle
            dataset_slug = "ingjuanrivera/work/collections/14823882"
            if upload_to_kaggle(temp_file_path, dataset_slug):
                st.success(f"{uploaded_file.name} uploaded successfully to Kaggle!")
            else:
                st.error(f"Failed to upload {uploaded_file.name}.")

            os.remove(temp_file_path)

    # Extraction button for feature processing
    if st.button('Analyze Document Content'):
        # Placeholder for document analysis functionality
        doc_intelligence = "Feature extraction and analysis results will be displayed here."
        st.success(doc_intelligence)
