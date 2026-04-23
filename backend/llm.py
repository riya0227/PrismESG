# llm.py

import os
import requests
import google.generativeai as genai


class HybridLLM:
    def __init__(self, mode="gemini"):
        self.mode = mode

        # -------- GEMINI SETUP --------
        if self.mode == "gemini":
            api_key = os.getenv("GOOGLE_API_KEY")

            if not api_key:
                raise ValueError("GOOGLE_API_KEY not set in environment")

            genai.configure(api_key=api_key)

            # safer model choice
            self.model = genai.GenerativeModel("gemini-1.5-flash")

    # -------- MAIN GENERATE FUNCTION --------
    def generate(self, prompt: str) -> str:

        if not prompt or not prompt.strip():
            return "Empty prompt provided."

        # ===== GEMINI =====
        if self.mode == "gemini":
            try:
                response = self.model.generate_content(prompt)

                if hasattr(response, "text") and response.text:
                    return response.text.strip()

                return "[Gemini Error] Empty response"

            except Exception as e:
                return f"[Gemini Error] {str(e)}"

        # ===== OLLAMA =====
        elif self.mode == "ollama":
            try:
                res = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "llama3",
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=60
                )

                res.raise_for_status()

                return res.json().get("response", "").strip() or "[Ollama Error] Empty response"

            except Exception as e:
                return f"[Ollama Error] {str(e)}"

        # ===== INVALID MODE =====
        else:
            return "Invalid LLM mode selected"