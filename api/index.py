import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 환경 변수에서 키 가져오기 (이름 상관없이 대응)
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# 모델 설정 (최신 안정 버전인 gemini-1.5-flash-latest 사용)
model = genai.GenerativeModel('gemini-1.5-flash')

def convert_text(text, target, lang='ko'):
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
        # 안전한 호출 방식 (API 버전에 따른 충돌 방지)
        response = model.generate_content(
            f"{system_instruction}\n\n변환할 문장: {text}",
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=1000,
                temperature=0.7
            )
        )
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
