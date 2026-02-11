import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 키 설정
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# [해결 포인트] 가장 호환성이 높은 모델명 'gemini-pro' 또는 'models/gemini-pro' 사용
model = genai.GenerativeModel('gemini-pro')

def convert_text(text, target, lang='ko'):
    if not api_key:
        return "API 키 설정이 필요합니다. Vercel 환경변수를 확인하세요."

    prompts = {
        "Boss": "격식 있는 비즈니스 보고 어투",
        "Colleague": "친근하고 예의 바른 동료 어투",
        "Customer": "매우 정중한 고객 응대 서비스 어투"
    }
    
    style = prompts.get(target, "비즈니스 어투")
    system_instruction = f"비즈니스 전문가로서 다음 문장을 {style}로 변환하세요. "
    system_instruction += "영어(English)로 응답하세요." if lang == 'en' else "한국어로 응답하세요."

    try:
        # 안전한 호출
        response = model.generate_content(f"{system_instruction}\n\n입력문장: {text}")
        return response.text.strip()
    except Exception as e:
        # 에러 메시지를 더 구체적으로 반환하여 디버깅 용이하게 함
        return f"AI 서비스 응답 오류: {str(e)}"

@app.route('/api/convert', methods=['POST'])
def convert():
    try:
        data = request.json
        input_text = data.get('text', '')
        target = data.get('target', 'Colleague')
        lang = data.get('lang', 'ko')
        
        result = convert_text(input_text, target, lang)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
