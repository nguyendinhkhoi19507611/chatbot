"""
LLM Service - Google Gemini 2.5 Flash integration

Priorities:
- Use Gemini to generate natural, helpful Vietnamese responses
- Fall back to local NLP/hybrid recommender when LLM isn't available
"""

import os
from typing import Optional

_gemini_ready = False
_gemini_model = None


def _lazy_init_gemini():
    global _gemini_ready, _gemini_model
    if _gemini_ready:
        return
    try:
        import google.generativeai as genai
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            # Also support .env loaded by python-dotenv if present
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            _gemini_ready = False
            return
        genai.configure(api_key=api_key)
        # Gemini 2.5 Flash model name may be exposed as below alias; keep adjustable by env
        model_name = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
        _gemini_model = genai.GenerativeModel(model_name)
        _gemini_ready = True
    except Exception as e:
        print(f"⚠ Gemini init failed: {e}")
        _gemini_ready = False


SYSTEM_PROMPT = (
    "Bạn là trợ lý tư vấn hướng nghiệp bằng tiếng Việt. "
    "Mục tiêu: trả lời ngắn gọn, hữu ích, có cấu trúc rõ ràng; "
    "khuyến khích người dùng chia sẻ sở thích, kỹ năng, mục tiêu. "
    "Khi phù hợp, đề xuất 2–3 nghề và gợi ý bước tiếp theo."
)


def generate_gemini_reply(user_message: str, context: Optional[str] = None) -> Optional[str]:
    """Return Gemini reply or None if unavailable/error."""
    _lazy_init_gemini()
    if not _gemini_ready or _gemini_model is None:
        return None
    try:
        content = f"<system>{SYSTEM_PROMPT}</system>\n"
        if context:
            content += f"<context>{context}</context>\n"
        content += f"<user>{user_message}</user>"
        res = _gemini_model.generate_content(content)
        if hasattr(res, 'text') and res.text:
            return res.text.strip()
        # Some SDK versions use candidates
        if getattr(res, 'candidates', None):
            parts = getattr(res.candidates[0], 'content', None)
            if parts and getattr(parts, 'parts', None):
                return ''.join(getattr(p, 'text', '') for p in parts.parts).strip()
    except Exception as e:
        print(f"Gemini error: {e}")
    return None


