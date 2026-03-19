import os
import shutil
import time
import base64
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

# Import your two logic files
from services.converter import convert_to_png
from services.processor import extract_elements

app = FastAPI()

UPLOAD_DIR = "storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def serve_index():
    # Attempt 1: Direct relative path (most reliable in Docker)
    index_path = "frontend/index.html"
    
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    # Attempt 2: Absolute path fallback
    base_path = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.join(base_path, "frontend", "index.html")
    
    if os.path.exists(absolute_path):
        return FileResponse(absolute_path)

    # If both fail, tell us WHERE it looked so we can fix the Dockerfile
    return {
        "error": "HTML not found",
        "checked_paths": [index_path, absolute_path],
        "current_directory": os.getcwd(),
        "directory_contents": os.listdir()
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    job_id = str(int(time.time()))
    file_extension = os.path.splitext(file.filename)[1].lower()
    input_path = os.path.join(UPLOAD_DIR, f"{job_id}{file_extension}")

    try:
        # 1. Save the uploaded file
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 2. Convert PDF/DOCX to a temporary PNG
        png_path = convert_to_png(input_path, job_id)

        if not png_path or not os.path.exists(png_path):
            raise HTTPException(status_code=500, detail="Conversion failed.")

        # 3. Use processor.py to cut the image and get the Base64 data
        # This returns the exact dictionary: {header_text, header_img, etc.}
        result_data = extract_elements(png_path)

        return result_data

    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    # This version is perfect for Render
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
