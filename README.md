# 📑 DocIntel AI Pipeline

[![Live Demo](https://img.shields.io/badge/Live-Application-brightgreen?style=for-the-badge&logo=render&logoColor=white)](https://documentextractor-mbx5.onrender.com/)
[![Docker CI with Pytest](https://github.com/syang48/DocumentExtractor/actions/workflows/pytest.yml/badge.svg)](https://github.com/syang48/DocumentExtractor/actions/workflows/pytest.yml)

**DocIntel AI** is a high-precision pipeline that surgically extracts headers and signatures from unstructured documents. By pairing **LibreOffice** normalization with **Amazon Textract** spatial intelligence, it delivers pixel-perfect results from even the messiest real-world files.

<img width="642" alt="DocIntel Interface" src="https://github.com/user-attachments/assets/c7a7df7c-2dd6-445d-9add-05c866ecb7cf" />

---

## 🚀 The Technical Pipeline

### 1. Ingestion & Normalization
The **FastAPI** backend accepts `.docx` and `.pdf` uploads. 
* **LibreOffice Headless** converts files to standard PDFs.
* **PyMuPDF** rasterizes them into high-res PNGs for visual mapping.

### 2. Spatial Intelligence (AWS Textract)
The system maps the document's DNA using deep learning to identify precise BoundingBox coordinates $(x, y, w, h)$.

<img width="457" alt="Textract Analysis" src="https://github.com/user-attachments/assets/a56c9891-82ac-4f7d-b5c3-b1c33189156e" />

### 3. Targeted Extraction
* **Header_Extractor:** Isolates metadata and branding from the top margin.
* **Signature_Extractor:** Pinpoints and crops legal signature blocks via **OpenCV** for lossless, high-quality output.

---

## 🗄️ Record Management
The **Record Tab** provides a robust management layer for auditing and asset recall.

<img width="702" alt="Records Management" src="https://github.com/user-attachments/assets/ec370821-584e-4e77-ad01-a18cfad42d9b" />

* **Audit Logs:** Full metadata indexing for every processed file.
* **Asset Persistence:** Download previous extractions without re-running AWS Textract analysis.

---

## 🛠 Tech Stack

* **AI/ML Analysis:** Amazon Textract — Deep learning for layout and coordinate extraction.
* **Development Assistance:** Google Gemini — Architectural guidance and algorithmic optimization.
* **Backend:** FastAPI, Docker, Render.
* **Processing:** LibreOffice (Conversion), PyMuPDF (Rasterization), OpenCV (Computer Vision).

---

**Stop mining for data. Start extracting it.**
