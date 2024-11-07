from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import tensorflow as tf
from PIL import Image
import pytesseract
import tempfile
import fitz  # PyMuPDF for handling PDFs
import shutil

app = FastAPI()

# Load the pre-trained model
working_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(working_dir, 'saved_models', 'doc_intelligence_model.keras')

# Ensure the model path exists or load the model
if not os.path.exists(model_path):
    raise HTTPException(status_code=500, detail="Model file not found.")
else:
    doc_intelligence_model = tf.keras.models.load_model(model_path)

# Helper function to save the uploaded file
def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(uploaded_file.file, temp_file)
        return temp_file.name

# Endpoint to upload and process files
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = save_uploaded_file(file)

    # Check file type and process accordingly
    if file.content_type.startswith("image/"):
        image = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(image)
        os.remove(file_path)
        return JSONResponse(content={"text": extracted_text if extracted_text else "No text found."})

    elif file.content_type == "application/pdf":
        doc_text = ""
        pdf = fitz.open(file_path)
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            doc_text += page.get_text("text")
        pdf.close()
        os.remove(file_path)
        return JSONResponse(content={"text": doc_text if doc_text else "No text found in PDF."})

    else:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Unsupported file type.")

# Endpoint to analyze document content
@app.post("/analyze/")
async def analyze_document(file: UploadFile = File(...)):
    file_path = save_uploaded_file(file)
    
    # Assuming `doc_intelligence` involves feature extraction
    doc_intelligence = "Feature extraction and analysis results for uploaded document."
    
    # Clean up the temporary file after processing
    os.remove(file_path)
    return JSONResponse(content={"analysis": doc_intelligence})

