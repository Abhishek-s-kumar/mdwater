#!/usr/bin/env python3
"""
Add watermark to PDF files - places watermark diagonally across pages
"""

import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import gray
from reportlab.lib.utils import simpleSplit
from io import BytesIO

def add_watermark_to_pdf(input_pdf_path, output_pdf_path, watermark_text, 
                        font_size=40, opacity=0.15, angle=45):
    """
    Add a diagonal text watermark to a PDF file
    
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
        
        # Get page dimensions
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        
        # Use appropriate page size
        if page_width > page_height:
            pagesize = (page_width, page_height)
        else:
            pagesize = (page_height, page_width)
        
        can = canvas.Canvas(packet, pagesize=pagesize)
        
        # Set watermark properties
        can.setFont("Helvetica-Bold", font_size)
        can.setFillColor(gray, alpha=opacity)
        
        # Calculate center position
        can.saveState()
        can.translate(page_width / 2, page_height / 2)
        can.rotate(angle)
        
        # Calculate text width
        text_width = can.stringWidth(watermark_text, "Helvetica-Bold", font_size)
        
        # Draw watermark multiple times for full page coverage
        # Create a grid pattern
        rows = 5
        cols = 3
        
        for row in range(-rows, rows + 1):
            for col in range(-cols, cols + 1):
                x_offset = col * (text_width + 200)  # Horizontal spacing
                y_offset = row * (font_size * 3)     # Vertical spacing
                can.drawString(x_offset - text_width/2, y_offset, watermark_text)
        
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
