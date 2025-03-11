#! /usr/bin/env python3

import fitz  # PyMuPDF
import argparse

# Define highlight colors in RGB format (0-1 range)
PALE_HIGHLIGHT_COLORS = [
    (1, 1, 0.6),    # Pale Yellow
    (1, 0.85, 0.6), # Pale Orange
    (1, 0.6, 0.6),  # Pale Red
    (0.6, 0.8, 1),  # Pale Blue
    (0.6, 1, 0.6)   # Pale Green
]

def load_words(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().lower() for line in file if line.strip()]

def highlight_words_in_pdf(input_pdf, output_pdf, words_to_highlight):
    doc = fitz.open(input_pdf)
    color_count = len(PALE_HIGHLIGHT_COLORS)

    for page in doc:
        words_on_page = page.get_text("words")
        for word in words_on_page:
            word_text = word[4].lower()
            if word_text in words_to_highlight:
                rect = fitz.Rect(word[:4])
                color = PALE_HIGHLIGHT_COLORS[hash(word_text) % color_count]
                highlight = page.add_highlight_annot(rect)
                highlight.set_colors(stroke=color)
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
