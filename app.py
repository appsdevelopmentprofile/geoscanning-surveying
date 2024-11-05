# -*- coding: utf-8 -*-
"""streamlit_ocr_app.py

A Streamlit application for OCR tasks using Tesseract and Pytesseract.
"""

import pytesseract
import streamlit as st
from PIL import Image
import tempfile

# Set the Tesseract command path if needed (uncomment and set path for macOS)
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

# Set Streamlit page configuration
st.set_page_config(
    page_title="Tesseract OCR Demo",
    layout="wide"
)

st.title("Tesseract OCR Document Intelligence")

# Sidebar options for different OCR tasks
st.sidebar.header("OCR Options")
selected_option = st.sidebar.selectbox(
    "Choose OCR Output Type",
    [
        "Simple Text Extraction",
        "Bounding Boxes",
        "Verbose Data",
        "Orientation and Script Detection",
        "Generate Searchable PDF",
        "Generate HOCR",
        "Generate ALTO XML"
    ]
)

# File uploader for image
uploaded_file = st.file_uploader("Upload an Image", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    # Open and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Perform OCR based on selected option
    if selected_option == "Simple Text Extraction":
        extracted_text = pytesseract.image_to_string(image)
        st.subheader("Extracted Text:")
        st.write(extracted_text if extracted_text else "No text found.")
    
    elif selected_option == "Bounding Boxes":
        boxes = pytesseract.image_to_boxes(image)
        st.subheader("Bounding Boxes:")
        st.text(boxes)
    
    elif selected_option == "Verbose Data":
        data = pytesseract.image_to_data(image)
        st.subheader("Verbose OCR Data:")
        st.write(data)
    
    elif selected_option == "Orientation and Script Detection":
        osd = pytesseract.image_to_osd(image)
        st.subheader("Orientation and Script Detection:")
        st.text(osd)
    
    elif selected_option == "Generate Searchable PDF":
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
        st.download_button("Download PDF", data=pdf_bytes, file_name="ocr_output.pdf")
    
    elif selected_option == "Generate HOCR":
        hocr_data = pytesseract.image_to_pdf_or_hocr(image, extension='hocr')
        st.subheader("HOCR Output:")
        st.text(hocr_data)
    
    elif selected_option == "Generate ALTO XML":
        xml_data = pytesseract.image_to_alto_xml(image)
        st.subheader("ALTO XML Output:")
        st.text(xml_data)
    
    st.success(f"OCR Operation '{selected_option}' completed.")
