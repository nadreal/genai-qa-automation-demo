# tests/test_hypothesis_demo.py
from hypothesis import given, strategies as st
import re

def clean_text(text: str) -> str:
    """Remove special characters and multiple spaces."""
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

@given(st.text())
def test_clean_text_never_crashes(input_text):
    result = clean_text(input_text)
    assert isinstance(result, str)

@given(st.text())
def test_clean_text_has_no_special_chars(input_text):
    result = clean_text(input_text)
    assert re.match(r"^[a-zA-Z0-9\s]*$", result) is not None
