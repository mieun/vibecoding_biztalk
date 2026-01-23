# BizTone Converter Project Context

## Project Overview

**BizTone Converter** is a web-based AI tool designed to help users convert informal text into professional business language. It targets new employees, junior staff, and anyone needing assistance with business communication.

*   **Goal:** Convert text to "Boss" (Formal/Report), "Colleague" (Polite/Request), or "Customer" (Service/Honorific) tones.
*   **Core Technology:**
    *   **Frontend:** HTML5, Tailwind CSS (via Play CDN), Vanilla JavaScript.
    *   **Backend:** Python (Flask), acting as an API gateway to the AI model.
    *   **AI Engine:** Groq API (using `llama-3.3-70b-versatile`).
    *   **Deployment:** Vercel (Serverless Functions).

## Architecture & Directory Structure

The project follows a Vercel-friendly structure where the API and static assets are served together.

```text
C:\vibecoding\biztalk_python\
├── api/                  # Backend Logic (Serverless Functions)
│   ├── index.py          # Main Flask Application Entry Point
│   ├── services.py       # Groq AI Integration & Prompt Engineering
│   └── requirements.txt  # Python Dependencies
├── public/               # Frontend Static Assets
│   ├── index.html        # Main SPA Entry Point (Tailwind CSS included)
│   └── js/
│       └── script.js     # Frontend Logic (DOM, Fetch API)
├── .venv/                # Local Python Virtual Environment
├── vercel.json           # Vercel Deployment Configuration
├── PRD.md                # Product Requirements Document
└── 프로그램개요서.md       # Initial Project Outline
```

## Key Files

*   **`api/index.py`**: The Flask app. It serves the static `index.html` at the root `/` and provides the `/api/convert` endpoint.
*   **`api/services.py`**: Contains the `convert_text` function which interacts with the Groq API. It defines the specific system prompts for each target audience (Boss, Colleague, Customer).
*   **`public/index.html`**: The user interface. Styled with Tailwind CSS v4 (Play CDN). Features a responsive top-down layout (Input -> Controls -> Output).
*   **`public/js/script.js`**: Handles user input, sends async requests to the backend, updates the UI with results, and manages the toast notifications.
*   **`vercel.json`**: Configures Vercel to treat `api/index.py` as a serverless function and route API traffic correctly.

## Setup & Development

### Prerequisites
*   Python 3.11+
*   Node.js (optional, for Vercel CLI)
*   Groq API Key

### Local Development
1.  **Environment:** Ensure the `.venv` is active.
2.  **Dependencies:** Install from `api/requirements.txt`.
    ```bash
    pip install -r api/requirements.txt
    ```
3.  **Environment Variables:** Create a `.env` file (or set system vars) with:
    ```
    GROQ_API_KEY=your_groq_api_key_here
    ```
4.  **Run Server:**
    ```bash
    python api/index.py
    ```
    The server typically runs at `http://localhost:5000`.

### Deployment (Vercel)
The project is configured for Vercel.
*   **Command:** `vercel` (to deploy) or `vercel dev` (for local simulation).
*   **Configuration:** Ensure the `GROQ_API_KEY` is added to the Vercel Project Settings > Environment Variables.

## Current Status & Conventions

*   **Styling:** We recently migrated from custom CSS to **Tailwind CSS**. All styling is done via utility classes in HTML. The layout is **Top-Down** (Input top, Output bottom).
*   **Responsiveness:** The UI is fully responsive, using `min-w-0` and `w-full` to ensure textareas shrink correctly on small screens.
*   **Backend Logic:** The "Sprint 3" logic (AI integration) is fully implemented in `api/services.py`.
*   **Language:** The codebase uses English for variable names/comments but the application interface and prompts are targeted at **Korean** users.

## Next Steps
*   **Deploy:** Push to Vercel and verify production behavior.
*   **Test:** Perform end-to-end testing on the live URL.
*   **Feedback:** Gather user feedback on the translation quality (Prompt Tuning).
