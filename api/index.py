from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- [여기가 노션에서 참고한 변환 로직입니다] ---
def convert_text(text):
    """
    비즈톡 텍스트를 파싱하여 원하는 형식으로 변환하는 함수
    (노션 예제 로직을 바탕으로 구현)
    """
    if not text:
        return ""
    
    # 예: 줄바꿈 처리나 비즈톡 특유의 형식을 변환하는 로직
    # 교육에서 배운 구체적인 변환 규칙이 있다면 이 부분을 수정하세요.
    lines = text.strip().split('\n')
    processed_lines = [f" {line}" for line in lines]
    return "\n".join(processed_lines)
# ----------------------------------------------

@app.route('/api/convert', methods=['POST'])
def convert():
    try:
        data = request.json
        input_text = data.get('text', '')
        
        # 위에서 만든 함수를 직접 호출
        result = convert_text(input_text)
        
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel이 실행할 서버 객체
if __name__ == "__main__":
    app.run(debug=True)
