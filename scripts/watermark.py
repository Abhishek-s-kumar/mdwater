#!/usr/bin/env python3
"""
Main PDF generation orchestrator
"""

import os
import sys
import json
import subprocess

def convert_md_to_pdf(md_file, pdf_file):
    """Convert markdown to PDF using pandoc"""
    os.makedirs(os.path.dirname(pdf_file), exist_ok=True)
    
    cmd = [
        'pandoc', md_file,
        '-o', pdf_file,
        '--pdf-engine=xelatex',
        '-V', 'geometry:margin=1in',
        '-V', 'fontsize=11pt',
        '--toc',
        '--toc-depth=3'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ✗ Pandoc failed: {result.stderr}")
        return False
    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_pdfs.py '<files_json>' '<watermark_text>'")
        sys.exit(1)
    
    files_json = sys.argv[1]
    watermark_text = sys.argv[2]
    
    try:
        files = json.loads(files_json)
    except:
        print("Invalid JSON input")
        sys.exit(1)
    
    if not files:
        print("No files to process")
        return
    
    print(f"Processing {len(files)} file(s)...")
    
    for md_file in files:
        if not os.path.exists(md_file):
            print(f"  ✗ File not found: {md_file}")
            continue
        
        # Output PDF path
        base_name = os.path.basename(md_file).replace('.md', '.pdf')
        pdf_file = f"generated-pdfs/{base_name}"
        
        print(f"\nProcessing: {md_file}")
        
        # Step 1: Convert to PDF
        if not convert_md_to_pdf(md_file, pdf_file):
            continue
        
        # Step 2: Add watermark using subprocess (no imports!)
        try:
            subprocess.run([
                sys.executable, 'scripts/watermark.py',
                pdf_file, pdf_file, watermark_text
            ], check=True)
            print(f"  ✓ Watermarked: {pdf_file}")
        except subprocess.CalledProcessError:
            print(f"  ✗ Watermark failed for: {pdf_file}")
            os.remove(pdf_file)  # Clean up failed file

if __name__ == "__main__":
    main()