"""
Tests for utils/validators.py
"""
import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.validators import is_valid_url, is_valid_email, is_valid_date_string, validate_document


class TestIsValidUrl:
    """Tests for is_valid_url function"""
    
    def test_valid_https_url(self):
        assert is_valid_url("https://www.example.com") is True
    
    def test_valid_http_url(self):
        assert is_valid_url("http://example.com/path") is True
    
    def test_valid_url_with_path(self):
        assert is_valid_url("https://patents.google.com/patent/US12345678") is True
    
    def test_invalid_url_no_scheme(self):
        assert is_valid_url("www.example.com") is False
    
    def test_invalid_url_ftp(self):
        assert is_valid_url("ftp://files.example.com") is False
    
    def test_empty_string(self):
        assert is_valid_url("") is False
    
    def test_none_value(self):
        assert is_valid_url(None) is False
    
    def test_non_string(self):
        assert is_valid_url(12345) is False


class TestIsValidEmail:
    """Tests for is_valid_email function"""
    
    def test_valid_email(self):
        assert is_valid_email("user@example.com") is True
    
    def test_valid_email_with_dots(self):
        assert is_valid_email("user.name@example.co.uk") is True
    
    def test_invalid_email_no_at(self):
        assert is_valid_email("userexample.com") is False
    
    def test_invalid_email_no_domain(self):
        assert is_valid_email("user@") is False
    
    def test_empty_string(self):
        assert is_valid_email("") is False


class TestIsValidDateString:
    """Tests for is_valid_date_string function"""
    
    def test_iso_format(self):
        assert is_valid_date_string("2026-02-06") is True
    
    def test_iso_with_time(self):
        assert is_valid_date_string("2026-02-06T10:30:00Z") is True
    
    def test_us_format(self):
        assert is_valid_date_string("02/06/2026") is True
    
    def test_invalid_format(self):
        assert is_valid_date_string("Feb 6, 2026") is False
    
    def test_empty_string(self):
        assert is_valid_date_string("") is False


class TestValidateDocument:
    """Tests for validate_document function"""
    
    def test_valid_document(self):
        doc = {
            "url": "https://example.com/article",
            "source": "Test Source",
            "title": "This is a valid title",
            "text": "This is the article text that should be at least 50 characters long to pass validation.",
            "published_date": "2026-02-06"
        }
        assert validate_document(doc) is True
    
    def test_missing_url(self):
        doc = {
            "source": "Test Source",
            "title": "Valid Title",
            "text": "This is the article text that should be at least 50 characters long.",
            "published_date": "2026-02-06"
        }
        assert validate_document(doc) is False
    
    def test_short_title(self):
        doc = {
            "url": "https://example.com/article",
            "source": "Test Source",
            "title": "Hi",
            "text": "This is the article text that should be at least 50 characters long.",
            "published_date": "2026-02-06"
        }
        assert validate_document(doc) is False
    
    def test_short_text(self):
        doc = {
            "url": "https://example.com/article",
            "source": "Test Source",
            "title": "Valid Title Here",
            "text": "Short text",
            "published_date": "2026-02-06"
        }
        assert validate_document(doc) is False
    
    def test_invalid_url(self):
        doc = {
            "url": "not-a-valid-url",
            "source": "Test Source",
            "title": "Valid Title Here",
            "text": "This is the article text that should be at least 50 characters long.",
            "published_date": "2026-02-06"
        }
        assert validate_document(doc) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
