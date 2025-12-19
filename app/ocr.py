import pdfplumber
import pytesseract
from PIL import Image
import os


def extract_text_from_pdf(file_path: str) -> str:
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


def extract_text_from_image(file_path: str) -> str:
    with Image.open(file_path) as image:
        return pytesseract.image_to_string(image)


def extract_text(file_path: str) -> str:
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(file_path)

    raise ValueError("Unsupported file type")
