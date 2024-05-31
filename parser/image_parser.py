import fitz
import os
from utils.pdf_operations import extract_images


def parse_images_from_specsheets(base_directory):
    specsheet_directory = os.path.join(base_directory, "tmp")
    for filename in os.listdir(specsheet_directory):
        if filename.endswith(".pdf"):
            pdf_filepath = os.path.join(specsheet_directory, filename)
            output_directory = os.path.join(base_directory, "images", os.path.basename(pdf_filepath).replace(".pdf", ""))
            extract_images(pdf_filepath, output_directory, filename.replace(".pdf", ""))
