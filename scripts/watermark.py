#!/usr/bin/env python3
"""
PDF watermarking utility
"""

import sys
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import gray
from io import BytesIO

def add_watermark_to_pdf(input_pdf_path, output_pdf_path, watermark_text):
    """Add a text watermark to a PDF file"""
    print(f"  Adding watermark: {watermark_text}")
    
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        
        # Get page dimensions
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        
        # Create watermark PDF
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        can.setFont('Helvetica-Bold', 40)
        can.setFillColor(gray, alpha=0.15)
        can.saveState()
        can.translate(page_width / 2, page_height / 2)
        can.rotate(45)
        
        # Draw watermark pattern
        for i in range(-2, 3):
            for j in range(-2, 3):
                x = i * 300
                y = j * 200
                can.drawString(x, y, watermark_text)
        
        can.restoreState()
        can.save()
        
        # Merge watermark
        packet.seek(0)
        watermark_pdf = PdfReader(packet)
        watermark_page = watermark_pdf.pages[0]
        page.merge_page(watermark_page)
        writer.add_page(page)
    
    # Write output
    with open(output_pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)
    
    print(f"  ✓ Watermarked PDF saved to: {output_pdf_path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python watermark.py <input_pdf> <output_pdf> <watermark_text>")
        sys.exit(1)
    
    add_watermark_to_pdf(sys.argv[1], sys.argv[2], sys.argv[3])