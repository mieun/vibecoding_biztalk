from api.services import convert_text
import sys

# Add the current directory to sys.path so we can import from api.services
sys.path.append('.')

def test_conversion():
    test_text = "이번 프로젝트 일정 좀 미뤄야 할 것 같아요. 너무 바빠서요."
    targets = ["boss", "colleague", "customer"]
    
    with open('test_output.txt', 'w', encoding='utf-8') as f:
        f.write(f"Original Text: {test_text}\n\n")
        
        for target in targets:
            f.write(f"--- Testing Target: {target} ---\n")
            try:
                result = convert_text(test_text, target)
                f.write(f"Result: {result}\n\n")
            except Exception as e:
                f.write(f"Error: {e}\n\n")

if __name__ == "__main__":
    test_conversion()
