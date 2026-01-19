#!/usr/bin/env python3
"""
Simple PDF watermarking using PyPDF2
"""

import os
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def create_watermark_pdf(text, page_width, page_height):
    """Create a simple watermark using reportlab if available"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.colors import gray
        
        packet = BytesIO()
        # Use the page dimensions
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))
        c.setFont("Helvetica", 20)
        c.setFillColor(gray, alpha=0.3)
        
        # Position watermark in center
        c.saveState()
        c.translate(page_width / 2, page_height / 2)
        c.rotate(45)
        
        # Draw watermark text
        c.drawString(-100, 0, text)
        c.restoreState()
        
        c.save()
        packet.seek(0)
        return packet
    except ImportError:
        print("⚠️  Reportlab not available, using simple text overlay")
        return None

def add_watermark_to_pdf(input_pdf_path, output_pdf_path, watermark_text):
    """
    Add a text watermark to a PDF file
    """
    print(f"Adding watermark: {watermark_text}")
    
    # Read the input PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        
        # Get page dimensions
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        
        # Create watermark
        watermark_packet = create_watermark_pdf(watermark_text, page_width, page_height)
        
        if watermark_packet:
            from PyPDF2 import PdfReader as WatermarkReader
            watermark_pdf = WatermarkReader(watermark_packet)
            watermark_page = watermark_pdf.pages[0]
            page.merge_page(watermark_page)
        
        writer.add_page(page)
    
    # Write the output PDF
    with open(output_pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)
    
    print(f"✓ Watermarked PDF saved to: {output_pdf_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python watermark.py <input_pdf> <output_pdf> <watermark_text>")
        sys.exit(1)
    
    add_watermark_to_pdf(sys.argv[1], sys.argv[2], sys.argv[3])
