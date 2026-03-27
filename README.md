# DocumentExtractor

Live Application: https://documentextractor-mbx5.onrender.com/

[![Docker CI with Pytest](https://github.com)]([![Docker CI with Pytest](https://github.com/syang48/DocumentExtractor/actions/workflows/pytest.yml/badge.svg)](https://github.com/syang48/DocumentExtractor/actions/workflows/pytest.yml))

DocumentExtractor is an automated pipeline designed to isolate high-value components (Headers and Signatures) from unstructured documents. By combining LibreOffice for robust format conversion and Amazon Textract for spatial intelligence, the system provides pixel-perfect extraction across various file types.

<img width="642" height="910" alt="Screenshot 2026-03-23 at 4 17 03 PM" src="https://github.com/user-attachments/assets/c7a7df7c-2dd6-445d-9add-05c866ecb7cf" />

The Technical Pipeline

1. Document Ingestion

The system features a FastAPI web interface that accepts high-volume uploads of both .docx and .pdf files.
2. Format Normalization (LibreOffice)

To ensure consistent analysis, all documents undergo a two-phase standardization process:

    Phase A: Incoming .docx files are processed via LibreOffice Headless to convert them into standard PDFs, preserving complex proprietary formatting.

    Phase B: The resulting PDF is rasterized into a high-resolution PNG using PyMuPDF (fitz) to prepare for visual coordinate mapping.

3. Spatial Analysis (AWS Textract)

The normalized PNG is analyzed by Amazon Textract. The service identifies text blocks and layout elements, returning precise BoundingBox coordinates:
(x,y,w,h)


<img width="457" height="764" alt="Screenshot 2026-03-23 at 4 16 21 PM" src="https://github.com/user-attachments/assets/a56c9891-82ac-4f7d-b5c3-b1c33189156e" />

4. Targeted Extraction

    Header_Extractor: Maps Textract coordinates to the document's top region to isolate metadata and letterheads.

    Signature_Extractor: Utilizes spatial pattern recognition to locate and isolate signature blocks.

5. Final Output

Using OpenCV, the service performs a lossless crop based on the identified coordinates, exporting the final results as individual, high-quality PNG files.



The platform includes a dedicated Record Tab, providing a robust management layer for previously processed work.

<img width="702" height="736" alt="Screenshot 2026-03-23 at 11 01 22 PM" src="https://github.com/user-attachments/assets/ec370821-584e-4e77-ad01-a18cfad42d9b" />


Document Logging: Every processed file is indexed with its original metadata for easy auditing.

History Tracking: Users can instantly revisit and review previously uploaded documents.

Asset Management: Extracted Header and Signature PNGs remain accessible for download without requiring a re-run of the Textract analysis.

Tech Stack

Core Infrastructure

    Backend: FastAPI (Python) – Asynchronous API framework.

    AI/ML Analysis: Amazon Textract – Deep learning for layout and coordinate extraction.

    Development Assistance: Google Gemini – Architectural guidance and algorithmic optimization.

Document & Image Processing

    Format Conversion: LibreOffice (Headless) – Proprietary .docx to .pdf conversion.

    PDF Manipulation: PyMuPDF – High-resolution rasterization.

    Computer Vision: OpenCV – Final coordinate-based image cropping.
