import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq  # Groq 라이브러리 필요

app = Flask(__name__)
CORS(app)

# Groq 클라이언트 설정 (Vercel 환경변수에서 키를 가져옴)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def convert_text(text, target, lang='ko'):
    """
    Groq AI를 사용하여 어투를 변환하는 핵심 로직
    """
    # 어투별 시스템 프롬프트 설정
    prompts = {
        "Boss": "보고 형식의 격식 있고 간결한 비즈니스 어투로 변환해줘. (Formal/Report)",
        "Colleague": "동료에게 요청하는 예의 바르면서도 친근한 어투로 변환해줘. (Polite/Request)",
        "Customer": "고객을 응대하는 매우 정중한 서비스 어투로 변환해줘. (Service/Honorific)"
    }
    
    system_prompt = prompts.get(target, prompts["Colleague"])
    if lang == 'en':
        system_prompt += " Please respond in English."
    else:
        system_prompt += " 반드시 한국어로 답변해줘."

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"다음 문장을 해당 어투로 변환해줘: {text}"}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI 변환 중 오류 발생: {str(e)}"

@app.route('/api/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        input_text = data.get('text', '')
        target = data.get('target', 'Colleague') # Boss, Colleague, Customer
        lang = data.get('lang', 'ko')

        if not input_text:
            return jsonify({"error": "내용을 입력해주세요."}), 400
            
        # AI 변환 실행
        result = convert_text(input_text, target, lang)
        
        # 프론트엔드 script.js가 'result' 키를 기다리므로 맞춰서 반환
        return jsonify({"result": result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
