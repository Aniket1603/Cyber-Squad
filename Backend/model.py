import cv2
import numpy as np
import exifread
import os

def get_metadata_score(file_stream):
    try:
        file_stream.seek(0)
        tags = exifread.process_file(file_stream, details=False)
        
        if not tags:
            return 95, "CRITICAL: Metadata is missing (Common in AI/Scrubbed media)."
        
        trust_tags = ['Image Make', 'Image Model', 'EXIF DateTimeOriginal']
        found = sum(1 for tag in trust_tags if tag in tags)
        
        software = str(tags.get('Image Software', '') or tags.get('Software', '')).lower()
        ai_tools = ['midjourney', 'dall-e', 'photoshop', 'firefly', 'stable diffusion']
        
        for tool in ai_tools:
            if tool in software:
                return 100, f"PROVEN AI: Metadata confirms {tool}."

        if found >= 2:
            return 0, "Authentic: Hardware metadata present."
        
        return 60, "Suspicious: Limited metadata (Possible export/edit)."
    except:
        return 80, "Error reading metadata."

def get_watermark_score(img_rgb):
    h, w, _ = img_rgb.shape
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    
    ch, cw = int(h * 0.15), int(w * 0.15)
    corners = [gray[0:ch, 0:cw], gray[0:ch, w-cw:w], gray[h-ch:h, 0:cw], gray[h-ch:h, w-cw:w]]

    corner_hits = 0
    for corner in corners:
        edges = cv2.Canny(corner, 100, 200)
        if (np.sum(edges) / corner.size) > 5.0:
            corner_hits += 1

    if corner_hits >= 2: return 95, f"AI Watermark/Logo patterns in {corner_hits} corners."
    if corner_hits == 1: return 50, "Potential watermark detected in one corner."
    return 0, "No visible watermarks."

def get_texture_score_from_buffer(img_bgr):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    noise_pattern = cv2.absdiff(gray, blurred)
    _, stddev = cv2.meanStdDev(noise_pattern)
    n_idx = stddev[0][0]

    if n_idx < 1.1: return 90, f"AI Smoothness (Noise: {round(n_idx,2)})"
    if n_idx < 2.8: return 45, f"Low Grain (Noise: {round(n_idx,2)})"
    return 0, f"Natural Grain (Noise: {round(n_idx,2)})"

def forensic_audit_web(file_storage):
    file_storage.seek(0)
    file_bytes = np.frombuffer(file_storage.read(), np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if img_bgr is None:
        return {"error": "Invalid Image"}

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    m_score, m_rep = get_metadata_score(file_storage)
    w_score, w_rep = get_watermark_score(img_rgb)
    t_score, t_rep = get_texture_score_from_buffer(img_bgr)

    final_score = (m_score * 0.5) + (w_score * 0.2) + (t_score * 0.3)

    return {
        "m_score": m_score, "m_rep": m_rep,
        "w_score": w_score, "w_rep": w_rep,
        "t_score": t_score, "t_rep": t_rep,
        "final_score": round(final_score, 2),
        "verdict": "AI-GENERATED" if final_score > 70 else "SUSPICIOUS" if final_score > 35 else "AUTHENTIC"
    }