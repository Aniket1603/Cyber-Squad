# 🔍 Image Forensic & AI Detection Toolkit

A comprehensive digital forensic suite designed to verify image authenticity, detect AI-generated content, and identify hidden digital manipulation through multi-layered analysis.

## 🌟 Overview

In an era of generative AI and sophisticated photo editing, this toolkit provides a technical layer of trust. It analyzes images through three primary lenses:
1.  **Metadata Integrity:** Checking for physical camera hardware signatures.
2.  **Noise Fingerprinting:** Identifying the presence (or absence) of natural sensor grain.
3.  **Visual Consistency:** Scanning for watermarks and structural anomalies.

---

## 🛠️ Features

### 1. Metadata & EXIF Audit
Scans the internal data of images to verify if they originated from a real-world camera.
* **Hardware Verification:** Looks for "Trust Tags" like Aperture, Shutter Speed, and Camera Model.
* **AI Tool Detection:** Identifies software signatures from Midjourney, DALL-E, Photoshop, and Stable Diffusion.
* **Scrubbing Detection:** Flags images that have had their metadata intentionally removed.

### 2. Texture & Noise Analysis (PRNU-based)
Analyzes the pixel-level variance to detect the "fingerprint" of a digital sensor.
* **High-Pass Filtering:** Isolates high-frequency noise by subtracting Gaussian blur.
* **Noise Indexing:** Real photos have chaotic, randomized grain; AI images often show "unnatural smoothness."
* **Forensic Heatmaps:** Generates a color-coded map showing where the image texture is consistent or manipulated.



### 3. Automated Watermark Detection
Uses computer vision to scan corners for logos, text overlays, or attribution marks.
* **Edge Density Analysis:** Utilizes Canny Edge Detection to find structured digital overlays in natural image corners.
* **Multi-Frame Support:** Capable of processing every frame in a GIF to ensure consistency.

---

## 🚀 Installation & Usage

### Prerequisites
Ensure you have Python 3.8+ and the following dependencies:
```bash
pip install opencv-python numpy Pillow exifread