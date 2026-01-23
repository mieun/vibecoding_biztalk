document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const sourceText = document.getElementById('source-text');
    const charCount = document.getElementById('char-count');
    const convertBtn = document.getElementById('convert-btn');
    const resultText = document.getElementById('result-text');
    const copyBtn = document.getElementById('copy-btn');
    const feedbackSection = document.getElementById('feedback-section');
    const toast = document.getElementById('toast');
    const langToggleBtn = document.getElementById('lang-toggle');
    
    // Constants
    const MAX_CHARS = 500;
    
    // Tailwind Class Strings
    const RESULT_PLACEHOLDER_CLASSES = ['bg-[#fafafa]', 'text-[#666666]'];
    const RESULT_TEXT_CLASSES = ['bg-white', 'text-[#333333]', 'border', 'border-[#E0E6ED]'];

    // Translations
    const translations = {
        en: {
            subtitle: "Transform your thoughts into perfect business language",
            inputTitle: "Input Text",
            placeholder: "Feel free to write what you want to say.\n(e.g., I think we need to delay the project schedule. I'm too busy.)",
            targetLabel: "Target Audience",
            optionBoss: "👔 Boss (Report/Formal)",
            optionColleague: "🤝 Colleague (Coop/Request)",
            optionCustomer: "🌟 Customer (Service/Polite)",
            convertBtn: "Convert",
            resultTitle: "Result",
            copyBtn: "Copy",
            resultPlaceholder: "Converted text will appear here.",
            feedbackGood: "👍 Helpful",
            feedbackBad: "👎 Not Helpful",
            toggleLabel: "한글", // Label to switch TO Korean
            
            // Dynamic Messages
            msgEnterText: "Please enter text to convert.",
            msgConverting: "Converting...",
            msgError: "Conversion failed.",
            msgServerError: "An error occurred. Please try again later.",
            msgConnError: "Failed to connect to server.",
            msgCopied: "Copied to clipboard! 📋",
            msgCopyFail: "Copy failed. Please copy manually.",
            msgFeedback: "Feedback sent. Thank you! 🙇"
        },
        ko: {
            subtitle: "나의 생각을 완벽한 비즈니스 언어로 변환하세요",
            inputTitle: "원문 입력",
            placeholder: "변환하고 싶은 내용을 자유롭게 작성해주세요.\n(예: 이번 프로젝트 일정 좀 미뤄야 할 것 같아요. 너무 바빠서요.)",
            targetLabel: "받는 사람",
            optionBoss: "👔 상사 (보고/격식)",
            optionColleague: "🤝 동료 (협업/요청)",
            optionCustomer: "🌟 고객 (응대/정중)",
            convertBtn: "변환하기",
            resultTitle: "변환 결과",
            copyBtn: "복사",
            resultPlaceholder: "변환된 텍스트가 여기에 표시됩니다.",
            feedbackGood: "👍 도움됨",
            feedbackBad: "👎 별로예요",
            toggleLabel: "English", // Label to switch TO English

            // Dynamic Messages
            msgEnterText: "변환할 내용을 입력해주세요.",
            msgConverting: "변환 중입니다...",
            msgError: "변환에 실패했습니다.",
            msgServerError: "오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
            msgConnError: "서버 연결에 실패했습니다.",
            msgCopied: "클립보드에 복사되었습니다! 📋",
            msgCopyFail: "복사에 실패했습니다. 직접 복사해주세요.",
            msgFeedback: "피드백이 전송되었습니다. 감사합니다! 🙇"
        }
    };

    let currentLang = localStorage.getItem('biztone-lang') || 'en';

    // Initialize Language
    setLanguage(currentLang);

    // Language Toggle
    langToggleBtn.addEventListener('click', () => {
        currentLang = currentLang === 'en' ? 'ko' : 'en';
        setLanguage(currentLang);
    });

    function setLanguage(lang) {
        localStorage.setItem('biztone-lang', lang);
        const t = translations[lang];

        // Update Toggle Button Text (Show the OTHER language)
        langToggleBtn.textContent = t.toggleLabel;

        // Update Static Text
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.dataset.i18n;
            if (t[key]) el.textContent = t[key];
        });

        // Update Placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.dataset.i18nPlaceholder;
            if (t[key]) el.placeholder = t[key];
        });
        
        // Update Result Placeholder if it is currently showing the placeholder text
        if (resultText.classList.contains(...RESULT_PLACEHOLDER_CLASSES)) {
             // We only update if it's the default placeholder text or the "Converting..." text from previous lang
             // But simpler is to just reset it if empty or matches old placeholder
             // For now, let's just update if it has the placeholder class.
             // Wait, if it says "Converting..." we don't want to change it to default placeholder immediately unless we track state.
             // Simplest approach: Update it if it's not the "active result" style.
             if (resultText.textContent === translations.en.resultPlaceholder || resultText.textContent === translations.ko.resultPlaceholder) {
                 resultText.textContent = t.resultPlaceholder;
             }
        }
    }

    function getMsg(key) {
        return translations[currentLang][key];
    }

    // 1. Character Count
    sourceText.addEventListener('input', () => {
        const currentLength = sourceText.value.length;
        charCount.textContent = `${currentLength}/${MAX_CHARS}`;
        
        if (currentLength > MAX_CHARS) {
            charCount.classList.remove('text-[#666666]');
            charCount.classList.add('text-red-500');
            sourceText.value = sourceText.value.substring(0, MAX_CHARS);
            charCount.textContent = `${MAX_CHARS}/${MAX_CHARS}`;
        } else {
            charCount.classList.remove('text-red-500');
            charCount.classList.add('text-[#666666]');
        }
    });

    // 2. Convert Action
    convertBtn.addEventListener('click', async () => {
        const text = sourceText.value.trim();
        const targetSelect = document.getElementById('target-select');
        const target = targetSelect.value;
        
        if (!text) {
            showToast(getMsg('msgEnterText'));
            sourceText.focus();
            return;
        }

        // UI Loading State
        setLoading(true);
        
        // Reset result area to placeholder style
        resultText.classList.remove(...RESULT_TEXT_CLASSES);
        resultText.classList.add(...RESULT_PLACEHOLDER_CLASSES);
        resultText.textContent = getMsg('msgConverting');
        
        copyBtn.disabled = true;
        feedbackSection.classList.add('hidden');

        try {
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text, target, lang: currentLang }),
            });

            const data = await response.json();

            if (response.ok) {
                // Success
                resultText.textContent = data.converted;
                
                // Change to result style
                resultText.classList.remove(...RESULT_PLACEHOLDER_CLASSES);
                resultText.classList.add(...RESULT_TEXT_CLASSES);
                
                copyBtn.disabled = false;
                feedbackSection.classList.remove('hidden');
            } else {
                // API Error
                throw new Error(data.error || getMsg('msgError'));
            }
        } catch (error) {
            console.error('Conversion Error:', error);
            resultText.textContent = getMsg('msgServerError');
            showToast(error.message || getMsg('msgConnError'));
        } finally {
            setLoading(false);
        }
    });

    // 3. Copy Action
    copyBtn.addEventListener('click', () => {
        const textToCopy = resultText.textContent;
        // Check if it's placeholder text
        if (!textToCopy || resultText.classList.contains('bg-[#fafafa]')) return;

        navigator.clipboard.writeText(textToCopy).then(() => {
            showToast(getMsg('msgCopied'));
        }).catch(() => {
            showToast(getMsg('msgCopyFail'));
        });
    });

    // 4. Feedback Action
    document.querySelectorAll('.feedback-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const type = e.target.dataset.type;
            console.log(`User feedback: ${type}`);
            showToast(getMsg('msgFeedback'));
        });
    });

    // Helper Functions
    function setLoading(isLoading) {
        const btnText = convertBtn.querySelector('.btn-text');
        const spinner = convertBtn.querySelector('.spinner');
        
        if (isLoading) {
            convertBtn.disabled = true;
            btnText.style.display = 'none';
            spinner.classList.remove('hidden');
        } else {
            convertBtn.disabled = false;
            btnText.style.display = 'inline';
            spinner.classList.add('hidden');
        }
    }

    let toastTimeout;
    function showToast(message) {
        toast.textContent = message;
        
        // Reset
        clearTimeout(toastTimeout);
        toast.classList.remove('hidden');
        // Force reflow
        void toast.offsetWidth; 
        
        // Fade In
        toast.classList.remove('opacity-0');
        
        // Schedule Fade Out
        toastTimeout = setTimeout(() => {
            toast.classList.add('opacity-0');
            setTimeout(() => {
                toast.classList.add('hidden');
            }, 300); // match transition duration
        }, 3000);
    }
});
