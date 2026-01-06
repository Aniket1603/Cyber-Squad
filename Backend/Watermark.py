import cv2
import numpy as np
from PIL import Image
import os

def detect_watermark(image_rgb):
    h, w, _ = image_rgb.shape
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    
    corner_h, corner_w = int(h * 0.15), int(w * 0.15)
    corners = [
        gray[0:corner_h, 0:corner_w],
        gray[0:corner_h, w-corner_w:w],
        gray[h-corner_h:h, 0:corner_w],
        gray[h-corner_h:h, w-corner_w:w]
    ]

    score = 0
    reasons = []

    for i, corner in enumerate(corners):
        edges = cv2.Canny(corner, 100, 200)
        density = np.sum(edges) / (corner.size)
        if density > 5.0:
            score += 25
            reasons.append(f"Corner {i+1} has high edge density (Possible logo/text).")

    if score > 70:
        final_score = 95
        report = "CRITICAL: Multiple watermark-like structures detected."
    elif score > 0:
        final_score = 50
        report = f"SUSPICIOUS: Potential logo or watermark: {reasons}"
    else:
        final_score = 0
        report = "No visible watermarks or logos detected in corners."

    return final_score, report

def check_image(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in ['.gif']:
        gif = Image.open(file_path)
        for frame_number in range(getattr(gif, "n_frames", 1)):
            gif.seek(frame_number)
            frame_rgb = np.array(gif.convert("RGB"))
            score, report = detect_watermark(frame_rgb)
            print(f"Frame {frame_number+1} Watermark Score: {score}")
            print(f"Frame {frame_number+1} Report: {report}\n")
    else:
        image = cv2.imread(file_path)
        if image is None:
            print("Failed to read the image.")
            return
        frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        score, report = detect_watermark(frame_rgb)
        print(f"Watermark Detection Score: {score}")
        print(f"Report: {report}")

file_path = r"C:\Users\ASUS\Downloads\Copy of IMG_2373.JPG"
check_image(file_path)