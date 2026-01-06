import io
from model import forensic_audit_web

class MockFileStorage:
    def __init__(self, file_path):
        with open(file_path, 'rb') as f:
            self.data = f.read()
        self.filename = file_path
        self.stream = io.BytesIO(self.data)

    def read(self, *args, **kwargs):
        return self.stream.read(*args, **kwargs)

    def seek(self, *args, **kwargs):
        return self.stream.seek(*args, **kwargs)

def test_single_image(path):
    print(f"--- ANALYZING: {path} ---")
    
    mock_file = MockFileStorage(path)
    
    result = forensic_audit_web(mock_file)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"VERDICT     : {result['verdict']}")
        print(f"FINAL SCORE : {result['final_score']}/100")
        print(f"METADATA    : {result['m_rep']} (Score: {result['m_score']})")
        print(f"TEXTURE     : {result['t_rep']} (Score: {result['t_score']})")
    print("-" * 50)

if __name__ == "__main__":
    target_image = r"C:\Users\ASUS\Downloads\raktmitralogo.png"
    test_single_image(target_image)