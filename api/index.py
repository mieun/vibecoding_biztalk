from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

app = Flask(__name__)
CORS(app) # 프론트엔드와 통신을 위해 필수입니다.

def convert_text(text):
    if not text:
        return ""
    # 여기에 실제 변환 로직이 들어갑니다.
    # 일단은 작동 확인을 위해 간단한 말머리를 붙이도록 설정했습니다.
    return f"[변환완료]\n{text}"

@app.route('/api/convert', methods=['POST'])
def convert():
    try:
        # 1. JSON 데이터 가져오기
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        input_text = data.get('text', '')
        
        # 2. 변환 함수 호출
        result = convert_text(input_text)
        
        # 3. 결과 반환
        return jsonify({"result": result})
        
    except Exception as e:
        # 에러 발생 시 로그에 상세 내용을 찍고 500 에러 반환
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Vercel이 이 파일을 읽을 때 app 객체를 직접 찾을 수 있도록 합니다.
# 파일 끝에 아무것도 추가하지 않아도 app 변수만 있으면 작동합니다.
