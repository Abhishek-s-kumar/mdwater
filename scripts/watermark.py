#!/usr/bin/env python3
"""
Add watermark to PDF files using PyPDF2 and reportlab
"""

import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import gray
from io import BytesIO

def add_watermark_to_pdf(input_pdf_path, output_pdf_path, watermark_text, 
                        font_size=40, opacity=0.2, angle=45):
    """
    Add a text watermark to a PDF file
    
    Args:
        input_pdf_path: Path to input PDF
        output_pdf_path: Path to save watermarked PDF
        watermark_text: Text to use as watermark
        font_size: Font size for watermark
        opacity: Opacity of watermark (0.0 to 1.0)
        angle: Rotation angle of watermark
    """
    
    # Read the input PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    # Create watermark PDF for each page
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        
        # Create a temporary watermark PDF with reportlab
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        
        # Set watermark properties
        can.setFont("Helvetica", font_size)
        can.setFillColor(gray, alpha=opacity)
        
        # Get page dimensions
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        
        # Calculate center position
        can.saveState()
        can.translate(page_width / 2, page_height / 2)
        can.rotate(angle)
        
        # Draw watermark text (centered and repeated for coverage)
        text_width = can.stringWidth(watermark_text, "Helvetica", font_size)
        
        # Create a grid of watermarks for better coverage
        for y in range(-2, 3):
            for x in range(-2, 3):
                offset_x = x * (text_width + 100)
                offset_y = y * (font_size * 2 + 50)
                can.drawString(offset_x - text_width/2, offset_y, watermark_text)
        
        can.restoreState()
        can.save()
        
        # Move to beginning of BytesIO buffer
        packet.seek(0)
        watermark_pdf = PdfReader(packet)
        watermark_page = watermark_pdf.pages[0]
        
        # Merge watermark with original page
        page.merge_page(watermark_page)
        writer.add_page(page)
    
    # Write the output PDF
    with open(output_pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)

if __name__ == "__main__":
    # Command line usage example
    import sys
    if len(sys.argv) < 4:
        print("Usage: python watermark.py <input_pdf> <output_pdf> <watermark_text>")
        sys.exit(1)
    
    add_watermark_to_pdf(sys.argv[1], sys.argv[2], sys.argv[3])
