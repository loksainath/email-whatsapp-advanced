from deep_translator import GoogleTranslator
from config import ENABLE_TRANSLATION, TARGET_LANGUAGE


def translate_text(text):
    if not text or not ENABLE_TRANSLATION:
        return text

    if TARGET_LANGUAGE.lower() == "en":
        return text

    text = text[:1000]  # safety limit

    try:
        return GoogleTranslator(
            source="auto",
            target=TARGET_LANGUAGE
        ).translate(text)
    except Exception as e:
        print("⚠ Translation skipped")
        return text
