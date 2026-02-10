import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# [수정된 부분] 환경 변수를 더 확실하게 가져오는 로직
def get_api_key():
    # 여러 이름의 후보군을 모두 뒤져서 하나라도 있으면 가져옵니다.
    keys = ["GEMINI_API_KEY", "GOOGLE_API_KEY"]
    for key_name in keys:
        val = os.environ.get(key_name)
        if val:
            return val.strip()  # 혹시 모를 앞뒤 공백 제거
    return None

api_key = get_api_key()

if api_key:
    genai.configure(api_key=api_key)
else:
    # 키가 없을 경우 서버 로그에 찍히도록 (Vercel Logs에서 확인 가능)
    print("CRITICAL ERROR: No API Key found in Environment Variables!")

model = genai.GenerativeModel('gemini-1.5-flash')

def convert_text(text, target, lang='ko'):
    if not api_key:
        return "서버 설정 오류: API 키를 찾을 수 없습니다. Vercel 환경 변수를 확인하세요."

    prompts = {
        "Boss": "보고 형식의 격식 있고 간결한 비즈니스 어투",
        "Colleague": "동료에게 요청하는 예의 바르면서도 친근한 어투",
        "Customer": "고객을 응대하는 매우 정중한 서비스 어투"
    }
    
    style = prompts.get(target, "비즈니스 어투")
    system_instruction = f"당신은 비즈니스 커뮤니케이션 전문가입니다. 다음 문장을 {style}로 변환하세요."
    
    if lang == 'en':
        system_instruction += " 응답은 반드시 영어(English)로만 작성하세요."
    else:
        system_instruction += " 응답은 반드시 한국어로만 작성하세요."

    try:
        response = model.generate_content(f"{system_instruction}\n\n변환할 문장: {text}")
        return response.text.strip()
    except Exception as e:
        return f"AI 서비스 응답 오류: {str(e)}"

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
        return jsonify({"result": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
