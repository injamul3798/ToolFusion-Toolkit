# ToolFusion: Convert, Resize, Record & PDFs

**ToolFusion** is a Streamlit web application that consolidates multiple utility tools into a single interface:

- **Notebook → Script Converter**: Extract and download Python code from a Jupyter notebook (`.ipynb`).
- **Image Resizer**: Resize images to custom dimensions and download the result.
- **Image Format Converter**: Convert uploaded images between formats (PNG, JPEG, GIF, BMP, TIFF, WEBP).
- **PDF → DOCX Converter**: Layout-preserving conversion of PDF documents to Word (`.docx`).
- **Screen Recorder**: Record your screen with audio, preview, and download as `.webm`.
- **Merge PDF Files**: Combine multiple PDFs into a single merged document.
- **Images → PDF Converter**: Batch-convert multiple images into a single PDF file.

---

## 🚀 Features

1. **Notebook to Script**: Extracts all code cells from an uploaded Jupyter Notebook and bundles them into a `.py` script.
2. **Image Resizing**: Preview original and resized images side-by-side, then download the new version.
3. **Format Conversion**: Seamlessly switch image formats, preserving quality.
4. **PDF to DOCX**: Uses `pdf2docx` to retain layout when converting PDFs to editable Word documents.
5. **Screen Recording**: Modern styled buttons to start/stop recording; generates a downloadable WebM clip.
6. **PDF Merger**: Upload and merge multiple `.pdf` files via `PyPDF2`’s `PdfMerger`.
7. **Images to PDF**: Convert a batch of images into one consolidated PDF using Pillow.

---
