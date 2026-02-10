import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Gemini 설정 (Vercel 환경변수에서 키를 가져옴)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def convert_text(text, target, lang='ko'):
    # 어투별 스타일 정의
    prompts = {
        "Boss": "보고 형식의 격식 있고 간결한 비즈니스 어투 (Formal/Report)",
        "Colleague": "동료에게 요청하는 예의 바르면서도 친근한 어투 (Polite/Request)",
        "Customer": "고객을 응대하는 매우 정중한 서비스 어투 (Service/Honorific)"
    }
    
    style = prompts.get(target, "예의 바른 비즈니스 어투")
    
    # AI에게 줄 지시문(Prompt)
    system_instruction = f"당신은 비즈니스 커뮤니케이션 전문가입니다. 다음 문장을 {style}로 변환하세요."
    if lang == 'en':
        system_instruction += " 응답은 반드시 영어(English)로만 작성하세요."
    else:
        system_instruction += " 응답은 반드시 한국어로만 작성하세요."

    try:
        # Gemini 모델 호출
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
            
        result = convert_text(input_text, target, lang)
        
        # 프론트엔드 data.result와 매칭
        return jsonify({"result": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
