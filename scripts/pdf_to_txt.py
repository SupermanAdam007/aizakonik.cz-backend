# brew install tesseract
# brew install tesseract-lang
import os

import pytesseract
from pdf2image import convert_from_path
from multiprocessing import Pool, freeze_support
import logging
import re


def process_page(args):
    page, page_number = args
    ocr_text = pytesseract.image_to_string(page, lang="ces")
    ocr_text = merge_hyphenated_words(ocr_text)
    logging.info(f"Processed page {page_number}")
    return ocr_text.strip()


def merge_hyphenated_words(text):
    # Match hyphenated words and join them back together
    merged_text = re.sub(r"(\w+)-\s*\n\s*([^\W\d_])", r"\1\2", text)
    return merged_text


def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    total_pages = len(images)

    with Pool() as pool:
        page_numbers = range(1, total_pages + 1)
        ocr_texts = pool.map(process_page, zip(images, page_numbers))

    text = "".join(ocr_texts)
    return text


if __name__ == "__main__":
    freeze_support()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logger = logging.getLogger(__name__)

    # Provide the path to your PDF file
    input_directory = 'data/pdfs'
    output_directory = 'data/txts'
    output_extension = '.txt'

    # Iterate over files in the directory
    for filename in os.listdir(input_directory):
        if os.path.isfile(os.path.join(input_directory, filename)):
            file_path = os.path.join(input_directory, filename)

            logger.info(f"Starting OCR extraction from file: {file_path}")

            result_text = extract_text_from_pdf(file_path)

            logger.info(f"OCR extraction of file {file_path} complete.")

            # Create the output file path with the same name and different extension
            output_filename = os.path.splitext(filename)[0] + output_extension
            output_file_path = os.path.join(output_directory, output_filename)

            with open(output_file_path, 'w') as f:
                f.write(result_text)
