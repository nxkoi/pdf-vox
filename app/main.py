from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

from app.pdf_processor import extract_text_and_images
from app.ai_client import process_with_ai

app = FastAPI(title="PDF-Vox", description="PDF processing with AI")

# Setup templates
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main upload page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Process uploaded PDF file"""
    try:
        # Save uploaded file temporarily
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Extract text and images from PDF
        result = extract_text_and_images(str(file_path))
        
        # Process with AI (placeholder)
        ai_result = process_with_ai(result["text"])
        
        # Clean up temporary file
        file_path.unlink()
        
        return {
            "filename": file.filename,
            "text": result["text"],
            "images_count": result["images_count"],
            "ai_response": ai_result
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

