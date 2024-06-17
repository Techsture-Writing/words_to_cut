#!/usr/bin/env python3


# Requirements:
# pip3 install pymupdf reportlab

import fitz
import argparse
import os


WORD_LIST = "words_to_cut.txt"

# Define highlight colors in RGB format (0-1 range)
PALE_HIGHLIGHT_COLORS = [
    (1, 1, 0.6),    # Pale Yellow
    (1, 0.85, 0.6), # Pale Orange
    (1, 0.6, 0.6),  # Pale Red
    (0.6, 0.8, 1),  # Pale Blue
    (0.6, 1, 0.6)   # Pale Green
]


def read_words_from_file(file_path):
    #Reads a list of words from a text file, removing only newline characters.
    with open(file_path, 'r') as file:
        words = [line.strip('\n') for line in file]
    return words


def main(input_pdf):
    # Read words to highlight from the text file
    words_to_highlight = read_words_from_file(WORD_LIST)    
    # Open the PDF
    pdf_document = fitz.open(input_pdf)
    color_index = 0
    # Iterate through pages
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        for word in words_to_highlight:
            text_instances = page.search_for(word)
            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors({"stroke": PALE_HIGHLIGHT_COLORS[color_index]})
                highlight.update()
                color_index = (color_index + 1) % len(PALE_HIGHLIGHT_COLORS)
    # Create the output file name
    base_name = os.path.splitext(input_pdf)[0]
    output_pdf = f"{base_name}_highlighted.pdf"
    # Save the new PDF
    pdf_document.save(output_pdf)
    print(f"Output saved to {output_pdf}")


if __name__ == '__main__':
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Highlight words in a PDF document.")
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    args = parser.parse_args()    
    main(args.input_pdf)
