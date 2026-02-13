"""
PDF Processing Module
Handles text extraction from PDF files with OCR fallback for scanned documents
"""

import pdfplumber
import os
from typing import Optional

def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """
    Extract text from a PDF file
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as string, or None if extraction fails
    """
    try:
        text = ""
        
        # Try extracting text using pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        
        # Check if we got meaningful text
        if text.strip():
            return text.strip()
        
        # If no text extracted, the PDF might be scanned
        # In a production environment, you would use OCR here
        # For now, return a message indicating OCR is needed
        return None
        
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return None

def extract_text_with_ocr(pdf_path: str) -> Optional[str]:
    """
    Extract text from scanned PDF using OCR
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as string, or None if extraction fails
    """
    try:
        # This would use pytesseract for OCR
        # Implementation would convert PDF pages to images and run OCR
        # For now, this is a placeholder
        
        from pdf2image import convert_from_path
        import pytesseract
        
        # Convert PDF to images
        images = convert_from_path(pdf_path)
        
        text = ""
        for i, image in enumerate(images):
            # Perform OCR on each page
            page_text = pytesseract.image_to_string(image)
            text += page_text + "\n\n"
        
        return text.strip() if text.strip() else None
        
    except Exception as e:
        print(f"Error performing OCR on PDF: {str(e)}")
        return None

def validate_pdf(pdf_path: str) -> bool:
    """
    Validate that the file is a valid PDF
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        True if valid PDF, False otherwise
    """
    try:
        if not os.path.exists(pdf_path):
            return False
        
        if not pdf_path.lower().endswith('.pdf'):
            return False
        
        # Try to open the PDF
        with pdfplumber.open(pdf_path) as pdf:
            # Check if it has at least one page
            return len(pdf.pages) > 0
            
    except Exception as e:
        print(f"PDF validation error: {str(e)}")
        return False

def get_pdf_metadata(pdf_path: str) -> dict:
    """
    Extract metadata from PDF file
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary containing PDF metadata
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            metadata = {
                'num_pages': len(pdf.pages),
                'metadata': pdf.metadata,
                'file_size': os.path.getsize(pdf_path)
            }
            return metadata
    except Exception as e:
        print(f"Error extracting PDF metadata: {str(e)}")
        return {}
