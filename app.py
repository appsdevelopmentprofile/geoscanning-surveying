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
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pytesseract
import tempfile
import fitz  # PyMuPDF for handling PDFs

# Set the Tesseract command path for macOS
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

# Set page configuration
st.set_page_config(
    page_title="AI - LiDAR, Photogrammetry, GNSS Positioning, Ground Penetrating Radar (GPR)",
    layout="wide",
    page_icon="🧑‍⚕️"
)

# Placeholder model setup to replace GCN
working_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(working_dir, 'doc_intelligence_model.keras')

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
        'AI - LiDAR, Photogrammetry, GNSS Positioning, Ground Penetrating Radar (GPR)',
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

    # Display the content of the file
    file_path = '/mnt/data/module1_CNN_documentation_intelligent_documents_reader (1).ipynb'
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            st.subheader("Content of the File:")
            st.text(content)
    except FileNotFoundError:
        st.error("File not found. Please ensure the file is in the correct path.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    # File uploader for multiple files
    uploaded_files = st.file_uploader("Upload your documents (images, PDFs)", type=['png', 'jpg', 'jpeg', 'pdf'], accept_multiple_files=True)

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

            os.remove(temp_file_path)

    # Extraction button for feature processing
    if st.button('Analyze Document Content'):
        # Placeholder for document analysis functionality
        doc_intelligence = "Feature extraction and analysis results will be displayed here."
        st.success(doc_intelligence)
