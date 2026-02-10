import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

def get_gemini_response(text, target, lang):
    # [핵심 수정] 함수가 실행될 때마다 환경 변수를 새로 읽어오도록 합니다.
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        return "에러: Vercel 환경 변수에 API 키가 설정되지 않았습니다."

    # API 키 설정
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompts = {
        "Boss": "보고 형식의 격식 있고 간결한 비즈니스 어투",
        "Colleague": "동료에게 요청하는 예의 바르면서도 친근한 어투",
        "Customer": "고객을 응대하는 매우 정중한 서비스 어투"
    }
    
    style = prompts.get(target, "비즈니스 어투")
    system_instruction = f"당신은 비즈니스 커뮤니케이션 전문가입니다. 다음 문장을 {style}로 변환하세요."
    system_instruction += " 응답은 반드시 영어로 하세요." if lang == 'en' else " 응답은 반드시 한국어로 하세요."

    try:
        response = model.generate_content(f"{system_instruction}\n\n변환할 문장: {text}")
        return response.text.strip()
    except Exception as e:
        return f"AI 변환 오류: {str(e)}"

@app.route('/api/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        input_text = data.get('text', '')
        target = data.get('target', 'Colleague')
        lang = data.get('lang', 'ko')

        if not input_text:
            return jsonify({"error": "내용을 입력해주세요."}), 400
            
        # 변환 함수 실행
        result = get_gemini_response(input_text, target, lang)
        
        return jsonify({"result": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
