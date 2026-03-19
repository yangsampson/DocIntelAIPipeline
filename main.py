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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(current_dir, "frontend", "index.html")
    if not os.path.exists(index_path):
        return {"error": "HTML file missing inside container"}
    return FileResponse(index_path)

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
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
