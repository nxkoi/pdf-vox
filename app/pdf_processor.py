import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, List


def extract_text_and_images(pdf_path: str) -> Dict:
    """
    Extract text and images from a PDF file using PyMuPDF.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary containing extracted text and image count
    """
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        text_content = []
        images_count = 0
        page_count = len(doc)
        
        # Extract text and images from each page
        for page_num in range(page_count):
            page = doc[page_num]
            
            # Extract text
            text = page.get_text()
            text_content.append(f"--- Page {page_num + 1} ---\n{text}\n")
            
            # Count images
            image_list = page.get_images()
            images_count += len(image_list)
        
        # Close the document
        doc.close()
        
        return {
            "text": "\n".join(text_content),
            "images_count": images_count,
            "pages": page_count
        }
    
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")


def extract_images(pdf_path: str, output_dir: str = "extracted_images") -> List[str]:
    """
    Extract images from PDF and save them to disk.
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save extracted images
        
    Returns:
        List of paths to extracted images
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    doc = fitz.open(pdf_path)
    image_paths = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            image_filename = f"page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
            image_path = output_path / image_filename
            
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
            
            image_paths.append(str(image_path))
    
    doc.close()
    return image_paths

