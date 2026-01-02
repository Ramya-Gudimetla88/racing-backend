import pytest
from datetime import date
from django.core.exceptions import ValidationError
from racing.models import validate_dob, validate_logo_size
from django.core.files.uploadedfile import SimpleUploadedFile
 
def test_validate_dob_valid():
    validate_dob(date(1995, 5, 20))  # should NOT raise
 
def test_validate_dob_invalid():
    with pytest.raises(ValidationError):
        validate_dob(date(2001, 1, 1))
 
def test_validate_logo_size_valid():
    image = SimpleUploadedFile(
        "logo.png",
        b"x" * (40 * 1024),  # 40 KB
        content_type="image/png"
    )
    validate_logo_size(image)
 
def test_validate_logo_size_invalid():
    image = SimpleUploadedFile(
        "logo.png",
        b"x" * (60 * 1024),  # 60 KB
        content_type="image/png"
    )
    with pytest.raises(ValidationError):
        validate_logo_size(image)
 