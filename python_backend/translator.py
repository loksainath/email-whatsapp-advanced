def translate_text(text: str, target_lang: str = "en") -> str:
    """
    Cloud-safe translation fallback.
    Returns original text.
    """
    if not text:
        return ""

    return text
