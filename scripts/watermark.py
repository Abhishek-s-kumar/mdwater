#!/usr/bin/env python3
"""
PDF watermarking utility - with proper content isolation
"""

import sys
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import gray
from io import BytesIO

def add_watermark_to_pdf(input_pdf_path, output_pdf_path, watermark_text):
    """Add a semi-transparent watermark that doesn't obscure content"""
    print(f"  Adding watermark: {watermark_text}")
    
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        
        # Get page dimensions
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        
        # Create watermark PDF with transparent background
        packet = BytesIO()
        
        # Calculate optimal font size (responsive to page)
        font_size = min(page_width / 20, 50)  # 1/20th of page width, max 50pt
        
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        
        # **KEY FIX**: Use 25% opacity (0.25 alpha) instead of 15%
        can.setFillColor(gray, alpha=0.25)
        can.setFont('Helvetica-Bold', font_size)
        can.saveState()
        
        # Center and rotate
        can.translate(page_width / 2, page_height / 2)
        can.rotate(45)
        
        # **KEY FIX**: Reduce pattern density (3x3 grid instead of 5x5)
        # Calculate spacing based on font size
        x_spacing = font_size * 6  # Wider horizontal gaps
        y_spacing = font_size * 4   # Wider vertical gaps
        
        # Draw watermark pattern (only 9 instances total)
        for i in range(-1, 2):  # -1, 0, 1 (3 columns)
            for j in range(-1, 2):  # -1, 0, 1 (3 rows)
                x = i * x_spacing
                y = j * y_spacing
                can.drawString(x, y, watermark_text)
        
        can.restoreState()
        can.save()  # This creates a transparent canvas
        
        # Merge watermark onto original page (overlay, not overwrite)
        packet.seek(0)
        watermark_pdf = PdfReader(packet)
        watermark_page = watermark_pdf.pages[0]
        
        # **IMPORTANT**: merge_page overlays transparent content correctly
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
