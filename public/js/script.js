document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const sourceText = document.getElementById('source-text');
    const charCount = document.getElementById('char-count');
    const convertBtn = document.getElementById('convert-btn');
    const resultText = document.getElementById('result-text');
    const copyBtn = document.getElementById('copy-btn');
    const feedbackSection = document.getElementById('feedback-section');
    const toast = document.getElementById('toast');
    
    // Constants
    const MAX_CHARS = 500;
    
    // 1. Character Count
    sourceText.addEventListener('input', () => {
        const currentLength = sourceText.value.length;
        charCount.textContent = `${currentLength}/${MAX_CHARS}`;
        
        if (currentLength > MAX_CHARS) {
            charCount.style.color = 'var(--color-error)';
            sourceText.value = sourceText.value.substring(0, MAX_CHARS);
            charCount.textContent = `${MAX_CHARS}/${MAX_CHARS}`;
        } else {
            charCount.style.color = 'var(--color-text-sub)';
        }
    });

    // 2. Convert Action
    convertBtn.addEventListener('click', async () => {
        const text = sourceText.value.trim();
        const targetOption = document.querySelector('input[name="target"]:checked');
        
        if (!text) {
            showToast('변환할 내용을 입력해주세요.');
            sourceText.focus();
            return;
        }

        if (!targetOption) {
            showToast('받는 사람을 선택해주세요.');
            return;
        }

        const target = targetOption.value;

        // UI Loading State
        setLoading(true);
        resultText.classList.remove('result-text');
        resultText.classList.add('result-placeholder');
        resultText.textContent = '변환 중입니다...';
        copyBtn.disabled = true;
        feedbackSection.classList.add('hidden');

        try {
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text, target }),
            });

            const data = await response.json();

            if (response.ok) {
                // Success
                resultText.textContent = data.converted;
                resultText.classList.remove('result-placeholder');
                resultText.classList.add('result-text');
                copyBtn.disabled = false;
                feedbackSection.classList.remove('hidden');
            } else {
                // API Error
                throw new Error(data.error || '변환에 실패했습니다.');
            }
        } catch (error) {
            console.error('Conversion Error:', error);
            resultText.textContent = '오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
            showToast(error.message || '서버 연결에 실패했습니다.');
        } finally {
            setLoading(false);
        }
    });

    // 3. Copy Action
    copyBtn.addEventListener('click', () => {
        const textToCopy = resultText.textContent;
        
        if (!textToCopy || resultText.classList.contains('result-placeholder')) return;

        navigator.clipboard.writeText(textToCopy).then(() => {
            showToast('클립보드에 복사되었습니다! 📋');
        }).catch(() => {
            showToast('복사에 실패했습니다. 직접 복사해주세요.');
        });
    });

    // 4. Feedback Action
    document.querySelectorAll('.feedback-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const type = e.target.dataset.type;
            console.log(`User feedback: ${type}`);
            showToast('피드백이 전송되었습니다. 감사합니다! 🙇');
            // Here you would typically send this to an analytics backend
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

    function showToast(message) {
        toast.textContent = message;
        toast.classList.remove('hidden');
        
        // Reset animation
        toast.style.animation = 'none';
        toast.offsetHeight; /* trigger reflow */
        toast.style.animation = null; 
    }
});
