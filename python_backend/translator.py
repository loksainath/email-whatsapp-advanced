# def translate_text(text: str, target_lang: str = "en") -> str:
#     """
#     Cloud-safe translation fallback.
#     Returns original text.
#     """
#     if not text:
#         return ""

#     return text


from config import ENABLE_TRANSLATION, TARGET_LANGUAGE

def translate_text(text: str, target: str | None = None) -> str:
    if not ENABLE_TRANSLATION or not text.strip():
        return text

    try:
        from deep_translator import GoogleTranslator
        lang = target or TARGET_LANGUAGE
        return GoogleTranslator(source="auto", target=lang).translate(text)
    except Exception as e:
        print(f"⚠ Translation skipped: {e}")
        return text
