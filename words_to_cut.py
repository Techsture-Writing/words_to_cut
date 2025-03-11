#! /usr/bin python3

# Requirements:
# pip3 install pymupdf reportlab

import fitz  # PyMuPDF
import re
import argparse

def load_words(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().lower() for line in file if line.strip()]

def highlight_words_in_pdf(input_pdf, output_pdf, words_to_highlight):
    doc = fitz.open(input_pdf)

    for page in doc:
        text_instances = []
        page_text = page.get_text("text")
        for word in words_to_highlight:
            for match in re.finditer(r'\b' + re.escape(word) + r'\b', page_text, re.IGNORECASE):
                start = match.start()
                end = match.end()
                text_instances.extend(page.search_for(page_text[start:end]))

        for inst in text_instances:
            highlight = page.add_highlight_annot(inst)
            highlight.update()

    doc.save(output_pdf, garbage=4, deflate=True)
    doc.close()

def main(input_pdf):
    output_pdf = "output_highlighted.pdf"
    words_file = "words_to_cut.txt"

    words_to_highlight = set(load_words(words_file))

    highlight_words_in_pdf(input_pdf, output_pdf, words_to_highlight)

    print(f"Highlighted PDF has been saved to {output_pdf}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Highlight words in a PDF document.")
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    args = parser.parse_args()
    main(args.input_pdf)
