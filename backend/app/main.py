from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
import os

# Initialize app
app = FastAPI()

# Folder to store uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 🏠 Root route - sanity check
@app.get("/")
def read_root():
    return {"message": "✅ Backend API running"}

# 📤 Upload files
@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    uploaded = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        uploaded.append(file.filename)
    return {"message": f"✅ Uploaded {len(uploaded)} files", "files": uploaded}

# 📃 List uploaded files with size
@app.get("/files")
async def list_files():
    try:
        files = os.listdir(UPLOAD_DIR)
        file_info = [
            {
                "name": f,
                "size_kb": round(os.path.getsize(os.path.join(UPLOAD_DIR, f)) / 1024, 2)
            }
            for f in files
        ]
        return JSONResponse(content={"files": file_info})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# 🗑️ Delete a file
@app.delete("/files/{filename}")
async def delete_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": f"✅ Deleted file {filename}"}
    else:
        return JSONResponse(status_code=404, content={"error": "File not found"})

# 🧠 Send file content to GPT (stub function included)
@app.post("/files/{filename}/gpt")
async def route_to_gpt(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        gpt_response = await call_gpt_model(content)
        return {"filename": filename, "gpt_response": gpt_response}
    else:
        return JSONResponse(status_code=404, content={"error": "File not found"})

# 👁️ Preview file contents
@app.get("/files/{filename}/preview")
async def preview_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"filename": filename, "content": content}
    else:
        return JSONResponse(status_code=404, content={"error": "File not found"})

# 🔧 GPT model call stub (replace with real API call later)
async def call_gpt_model(content: str) -> str:
    return f"🤖 GPT processed the file content (length: {len(content)} chars)"
# Note: This is a stub function. Replace with actual GPT API call logic.
# This function simulates a call to a GPT model and should be replaced with actual API logic.
# To run the app, use: uvicorn main:app --reload

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your Codespaces frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
