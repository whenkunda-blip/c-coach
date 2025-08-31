import pytest
import os
import tempfile
from text_processor import TextProcessor

class TestTextProcessor:
    
    def test_clean_text(self):
        """Test text cleaning functionality"""
        # Test with extra whitespace
        dirty_text = "  This   has    extra    spaces  "
        cleaned = TextProcessor.clean_text(dirty_text)
        assert cleaned == "This has extra spaces"
        
        # Test with special characters
        special_text = "Python@#$%^&*()_+{}|:<>?[]\\;'\",./"
        cleaned = TextProcessor.clean_text(special_text)
        assert cleaned == "Python()_:?;,."
        
        # Test with empty string
        assert TextProcessor.clean_text("") == ""
        assert TextProcessor.clean_text(None) == ""
    
    def test_extract_from_txt(self):
        """Test text file extraction"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test resume\nWith multiple lines\nPython, JavaScript, React")
            temp_file = f.name
        
        try:
            text = TextProcessor._extract_from_txt(temp_file)
            assert "This is a test resume" in text
            assert "Python, JavaScript, React" in text
        finally:
            os.unlink(temp_file)
    
    def test_extract_text_from_file_unsupported_format(self):
        """Test handling of unsupported file formats"""
        with pytest.raises(ValueError, match="Unsupported file format"):
            TextProcessor.extract_text_from_file("test.xyz")
    
    def test_extract_text_from_file_txt(self):
        """Test text file extraction through main method"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test resume content")
            temp_file = f.name
        
        try:
            text = TextProcessor.extract_text_from_file(temp_file)
            assert text == "Test resume content"
        finally:
            os.unlink(temp_file)
