import exifread
import os
from PIL import Image

def get_detailed_exif(image_path):
    print(f"\n[ forensic check ] Analyzing Metadata: {os.path.basename(image_path)}")
    
    score = 0
    reasons = []
    
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            
        if not tags:
            return 100, "CRITICAL: No EXIF metadata found. Extremely likely to be AI-generated, a screenshot, or scrubbed."

        trust_tags = {
            'Image Make': "Manufacturer info found.",
            'Image Model': "Camera model info found.",
            'EXIF DateTimeOriginal': "Original timestamp found.",
            'EXIF FNumber': "Aperture hardware data found.",
            'EXIF ExposureTime': "Shutter speed data found."
        }
        
        found_trust_tags = 0
        for tag, description in trust_tags.items():
            if tag in tags:
                found_trust_tags += 1
            else:
                reasons.append(f"Missing {tag}")

        software_tag = str(tags.get('Image Software', '')).lower()
        ai_tools = ['midjourney', 'stable diffusion', 'dall-e', 'adobe firefly', 'photoshop']
        
        for tool in ai_tools:
            if tool in software_tag:
                score = 100
                return score, f"PROVEN FAKE: Metadata explicitly mentions software: {software_tag}"

        if found_trust_tags >= 4:
            score = 0
            message = "AUTHENTIC: Strong hardware metadata present."
        elif found_trust_tags >= 2:
            score = 40
            message = f"SUSPICIOUS: Partial metadata found. Missing: {reasons}"
        else:
            score = 80
            message = f"HIGHLY SUSPICIOUS: Almost no hardware metadata. Missing: {reasons}"

        return score, message

    except Exception as e:
        return 50, f"ERROR: Could not read file metadata: {str(e)}"

if __name__ == "__main__":
    path = r"C:\Users\ASUS\Downloads\raktmitralogo.png"
    if os.path.exists(path):
        suspicion_score, report = get_detailed_exif(path)
        print(f"Suspicion Score: {suspicion_score}/100")
        print(f"Report: {report}")
    else:
        print("Invalid Path!")