# GR01_DATA
## 7 nov 2025
Andrey Cleaned data from original file.
we could chech witch file format (md or csv) are better to work with for ML
---
# Data Cleaning Pipeline: Structured Extraction with MarkItDown
## Overview
This document focuses exclusively on the extraction and sanitization of data from Excel files using Microsoft MarkItDown. While Python's pandas.read_excel is sufficient for simple spreadsheets, using MarkItDown allows for an intermediate Markdown representation, which can be useful for preserving document structure, metadata, or feeding the data into LLM (Large Language Model) contexts before structuring it into CSV.
## The Challenge
When converting rich documents or spreadsheets to Markdown, automated tools often insert styling artifacts.
Artifacts: Markdown table separators (|---|), extra newlines, or file metadata.
Goal: To strip these artifacts and produce a clean, machine-readable CSV file without losing data integrity (e.g., preserving UTF-8 characters and internal commas in comments).
The Solution Logic
Ingestion: Load the .xlsx file using MarkItDown.
Intermediate State: Convert to a raw text/Markdown string.
Filtering:
Identify lines starting with | (table rows).
Regex/String matching to identify and discard formatting rows (|---|).
Trim whitespace and empty lines.
Output: Write the clean data to a CSV file using pandas to handle delimiter escaping automatically.
Implementation Script
Save this as clean_data.py.
code
```Python
from markitdown import MarkItDown
import pandas as pd
import os

# CONFIGURATION
# Replace with your actual file name
INPUT_FILENAME = "Análise de Sentimento _ Hospital da Luz .xlsx"

# Auto-generate output filenames
base_name = os.path.splitext(INPUT_FILENAME)[0]
OUTPUT_MD_FILE = f"{base_name}_cleaned.md"
OUTPUT_CSV_FILE = "Cleaned_Data.csv"

def clean_and_convert():
    # 1. Convert Excel to Markdown
    print(f"Processing {INPUT_FILENAME}...")
    try:
        md_converter = MarkItDown()
        result = md_converter.convert(INPUT_FILENAME)
        raw_markdown = result.text_content
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # 2. Filter and Clean Lines
    lines = raw_markdown.split('\n')
    cleaned_lines = []
    
    # Logic: Keep lines that look like table rows or contain significant text
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') or stripped:
            cleaned_lines.append(line)
            
    clean_markdown_text = '\n'.join(cleaned_lines).strip()

    # Save the structural Markdown (optional, for reference)
    with open(OUTPUT_MD_FILE, "w", encoding="utf-8") as f:
        f.write(clean_markdown_text)
    print(f"Intermediate Markdown saved: {OUTPUT_MD_FILE}")

    # 3. Parse into CSV Format
    print("Extracting structured data...")
    table_rows = []
    
    for line in cleaned_lines:
        # Identify table rows based on pipe delimiters
        if line.strip().startswith('|') and line.strip().endswith('|'):
            # Split by pipe, remove the first and last empty elements
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            
            # CRITICAL STEP: Remove Markdown separator lines (e.g., "---", ":---")
            # If any cell contains "---", we assume it's a formatting row and skip it.
            if cells and not any('---' in cell for cell in cells):
                table_rows.append(cells)

    # 4. Save to CSV
    if len(table_rows) >= 2:
        headers = table_rows[0]
        data = table_rows[1:]
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=headers)
        
        # Post-processing (optional): Fill missing values
        df.fillna('', inplace=True)
        
        df.to_csv(OUTPUT_CSV_FILE, index=False, encoding="utf-8")
        print(f"Success! Clean data saved to: {OUTPUT_CSV_FILE}")
        print(f"Rows: {len(data)}, Columns: {len(headers)}")
        print("-" * 30)
        print("First 3 rows preview:")
        print(df.head(3).to_string(index=False))
    else:
        print("Error: Could not identify a valid table structure in the file.")

if __name__ == "__main__":
    clean_and_convert()
    
```
## Key Features of this Script
Robust Encoding: Uses utf-8 to ensure Portuguese characters (ã, é, ç) are preserved.
Separator Logic: The check if row and not any('---' in cell for cell in row) guarantees that Markdown styling does not leak into the final dataset.
Dual Output: Provides both a readable Markdown document and a strict CSV database.
