import cv2
import numpy as np

def analyze_texture_and_noise(image_path):
    img = cv2.imread(image_path)
    if img is None: return None, 0, "Invalid Path"
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    noise_pattern = cv2.absdiff(gray, blurred)
    
    mean, stddev = cv2.meanStdDev(noise_pattern)
    noise_index = stddev[0][0]
    
    noise_norm = cv2.normalize(noise_pattern, None, 0, 255, cv2.NORM_MINMAX)
    heatmap = cv2.applyColorMap(noise_norm.astype(np.uint8), cv2.COLORMAP_JET)
    
    overlay = cv2.addWeighted(img, 0.7, heatmap, 0.3, 0)
    
    score = 0
    if noise_index < 3.5:
        score = 95
        verdict = "CRITICAL: No physical sensor noise detected. Likely AI/Digital Graphic."
    elif noise_index < 7.0:
        score = 60
        verdict = "SUSPICIOUS: Unusually smooth. Possible AI or heavy post-processing."
    else:
        score = 10
        verdict = "AUTHENTIC: Natural camera sensor grain detected."

    output_filename = "forensic_analysis_result.png"
    cv2.imwrite(output_filename, overlay)
    
    return output_filename, score, verdict, round(noise_index, 2)

if __name__ == "__main__":
    path = r"C:\Users\ASUS\Downloads\Copy of IMG_2373.JPG"
    result_file, score, verdict, n_idx = analyze_texture_and_noise(path)
    
    print(f"\n" + "="*50)
    print(f"REPORT FOR: {path}")
    print(f"NOISE FINGERPRINT INDEX: {n_idx}")
    print(f"SUSPICION SCORE: {score}/100")
    print(f"FORENSIC VERDICT: {verdict}")
    print(f"HEATMAP SAVED TO: {result_file}")
    print("="*50)