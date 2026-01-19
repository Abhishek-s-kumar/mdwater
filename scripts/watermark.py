#!/usr/bin/env python3
"""
PDF watermarking utility - Single centered watermark with perfect spacing
"""

import sys
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import gray
from reportlab.pdfbase.pdfmetrics import stringWidth
from io import BytesIO

def add_watermark_to_pdf(input_pdf_path, output_pdf_path, watermark_text):
    """Add a single, large, semi-transparent watermark centered on each page"""
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
        
        # **OPTIMAL FONT SIZE**: 1/15th of page width (larger, but not overwhelming)
        font_size = min(page_width / 20, 60)  # Cap at 60pt
        
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        
        # **LIGHTER OPACITY**: 15% (0.15) for minimal content obstruction
        can.setFillColor(gray, alpha=0.15)
        can.setFont('Helvetica-Bold', font_size)
        can.saveState()
        
        # Center and rotate
        can.translate(page_width / 2, page_height / 2)
        can.rotate(45)
        
        # **PERFECT CENTERING**: Calculate exact text width
        text_width = stringWidth(watermark_text, 'Helvetica-Bold', font_size)
        
        # **SINGLE WATERMARK**: Draw once, perfectly centered
        can.drawString(-text_width / 2, 0, watermark_text)
        
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
