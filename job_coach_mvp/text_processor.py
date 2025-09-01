import pdfplumber
from docx import Document
import re
import os

class TextProcessor:
    """Handles text extraction from various file formats"""
    
    @staticmethod
    def extract_text_from_file(file_path):
        """Extract text from uploaded file based on file extension"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return TextProcessor._extract_from_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            return TextProcessor._extract_from_docx(file_path)
        elif file_extension in ['.txt']:
            return TextProcessor._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    @staticmethod
    def _extract_from_pdf(file_path):
        """Extract text from PDF using pdfplumber"""
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text.strip()
        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {str(e)}")
    
    @staticmethod
    def _extract_from_docx(file_path):
        """Extract text from Word document"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error extracting text from Word document: {str(e)}")
    
    @staticmethod
    def _extract_from_txt(file_path):
        """Extract text from plain text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            raise ValueError(f"Error reading text file: {str(e)}")
    
    @staticmethod
    def clean_text(text):
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation and letters/numbers
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
        
        # Clean up any remaining special characters that might have slipped through
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
        
        return text.strip()
