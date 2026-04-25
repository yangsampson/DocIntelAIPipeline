# 📑 DocIntel AI Pipeline

[![Live Demo](https://img.shields.io/badge/Live-Application-brightgreen?style=for-the-badge&logo=render&logoColor=white)](https://documentextractor-mbx5.onrender.com/)
[![Docker CI with Pytest](https://github.com/syang48/DocumentExtractor/actions/workflows/pytest.yml/badge.svg)](https://github.com/syang48/DocumentExtractor/actions/workflows/pytest.yml)

**DocIntel AI** is a high-precision automated pipeline engineered to surgically isolate high-value components—specifically **Headers and Signatures**—from unstructured documents. By orchestrating LibreOffice for robust normalization and Amazon Textract for spatial intelligence, the system delivers pixel-perfect extraction from messy, real-world files.

---

## 🚀 The Technical Pipeline

The system transforms raw, unstructured data into actionable visual assets through a five-stage specialized workflow:

### 1. Document Ingestion
A high-performance **FastAPI** interface handles concurrent uploads of `.docx` and `.pdf` files, providing immediate validation and queuing.

### 2. Format Normalization (The "Clean Room")
To ensure 100% analysis consistency, documents undergo a two-phase standardization:
* **Phase A:** Legacy `.docx` files are processed via **LibreOffice Headless** to maintain layout integrity during PDF conversion.
* **Phase B:** PDFs are rasterized into high-resolution PNGs via **PyMuPDF (fitz)**, creating a stable canvas for coordinate mapping.

### 3. Spatial Intelligence (AWS Textract)
The normalized image is analyzed by **Amazon Textract**. Rather than just performing simple OCR, the system extracts precise **BoundingBox** metadata:
$$Area = (x, y, width, height)$$
This spatial DNA allows the pipeline to "understand" exactly where components live on the page.

### 4. Targeted Extraction
Custom-built extractors apply logic to the spatial data:
* **Header_Extractor:** Maps top-region coordinates to isolate metadata and branding.
* **Signature_Extractor:** Utilizes spatial pattern recognition to pinpoint and crop legal signature blocks.

### 5. Final Output & Lossless Cropping
Using **OpenCV**, the pipeline performs a surgical, lossless crop based on the identified coordinates, exporting the final results as high-fidelity PNG assets.

---

## 🗄️ Record Management & Auditing

The platform features a dedicated **Records Tab**, serving as a robust management layer for your document history:

* **Audit Logging:** Every file is indexed with metadata for full traceability.
* **Instant Recall:** Revisit and review any previously processed document without re-processing.
* **Asset Persistence:** Extracted headers and signatures are stored and ready for download, eliminating redundant AWS Textract costs.

---

## 🛠 Tech Stack

### **Core Infrastructure**
* **Backend:** FastAPI (Python) - High-speed asynchronous API framework.
* **AI/ML Analysis:** Amazon Textract - Deep learning for layout and coordinate extraction.
* **Architectural Guidance:** Google Gemini - Algorithmic optimization and logic design.

### **Document & Image Processing**
* **Normalization:** LibreOffice (Headless) - Industry-standard document conversion.
* **Rasterization:** PyMuPDF - High-resolution PDF-to-image processing.
* **Computer Vision:** OpenCV - Coordinate-based image manipulation and cropping.

---

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/syang48/DocumentExtractor.git](https://github.com/syang48/DocumentExtractor.git)
   cd DocumentExtractor
