import os
import shutil
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

# 1. Setup Absolute Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv()

UPLOAD_DIR = os.path.join(BASE_DIR, os.getenv("UPLOAD_DIR", "storage/uploads"))
OUTPUT_DIR = os.path.join(BASE_DIR, os.getenv("OUTPUT_DIR", "storage/output"))

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Import logic files
from services.converter import convert_to_png
from services.processor import extract_elements

app = FastAPI()

# Pydantic model for Bulk Delete
class DeleteRequest(BaseModel):
    folders: List[str]

# --- PAGE ROUTES ---

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "frontend", "index.html"))

@app.get("/record")
async def serve_record():
    return FileResponse(os.path.join(BASE_DIR, "frontend", "record.html"))

# --- UPLOAD & ZIP DOWNLOAD ---

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    safe_filename = file.filename.replace(" ", "_")
    input_path = os.path.join(UPLOAD_DIR, safe_filename)
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        png_path = convert_to_png(input_path, safe_filename)
        if not png_path or not os.path.exists(png_path):
            raise HTTPException(status_code=500, detail="Conversion failed.")
            
        result_data = extract_elements(png_path)
        result_data["folder_id"] = safe_filename
        return result_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_output_folder(filename: str, background_tasks: BackgroundTasks):
    base_name = os.path.splitext(filename)[0]
    folder_path = os.path.join(OUTPUT_DIR, base_name)
    if not os.path.exists(folder_path):
        raise HTTPException(status_code=404, detail="Source folder not found.")
    
    zip_base_path = os.path.join(OUTPUT_DIR, f"{base_name}_temp")
    shutil.make_archive(zip_base_path, 'zip', folder_path)
    final_zip_path = f"{zip_base_path}.zip"
    
    background_tasks.add_task(os.remove, final_zip_path)
    return FileResponse(path=final_zip_path, filename=f"{base_name}_professional.zip", media_type="application/zip")

# --- INDIVIDUAL ASSET DOWNLOADS (PREVIEWS) ---

@app.get("/download/header/{base_name}")
async def download_header(base_name: str):
    clean_name = os.path.splitext(base_name)[0]
    file_path = os.path.join(OUTPUT_DIR, clean_name, f"{clean_name}_header.png")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Header not found.")
    return FileResponse(path=file_path, filename=f"{clean_name}_header.png", media_type="image/png")

@app.get("/download/signature/{base_name}")
async def download_signature(base_name: str):
    clean_name = os.path.splitext(base_name)[0]
    file_path = os.path.join(OUTPUT_DIR, clean_name, f"{clean_name}_signature.png")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Signature not found.")
    return FileResponse(path=file_path, filename=f"{clean_name}_signature.png", media_type="image/png")

# --- RECORD MANAGEMENT (API) ---

@app.get("/api/records")
async def get_records_data(page: int = 1, limit: int = 10):
    if not os.path.exists(OUTPUT_DIR): return {"records": [], "total": 0}
    all_folders = [f for f in os.listdir(OUTPUT_DIR) if os.path.isdir(os.path.join(OUTPUT_DIR, f))]
    all_folders.sort(key=lambda x: os.path.getmtime(os.path.join(OUTPUT_DIR, x)), reverse=True)
    
    total = len(all_folders)
    start = (page - 1) * limit
    paginated_folders = all_folders[start:start + limit]
    return {"records": paginated_folders, "total": total}

@app.post("/api/delete")
async def delete_records(data: DeleteRequest):
    """Handles both single and bulk deletion of record folders."""
    deleted_items = []
    for folder_name in data.folders:
        # Clean the name to prevent directory traversal
        clean_name = os.path.basename(folder_name)
        target_path = os.path.join(OUTPUT_DIR, clean_name)
        
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
            deleted_items.append(clean_name)
            
    return {"message": "Success", "deleted": deleted_items}

if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=DEBUG)
