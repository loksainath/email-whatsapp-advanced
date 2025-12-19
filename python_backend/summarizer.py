# from transformers import pipeline
# from config import ENABLE_SUMMARY

# _summarizer = None


# def summarize_text(text):
#     global _summarizer

#     if not text:
#         return ""

#     # Feature toggle
#     if not ENABLE_SUMMARY:
#         return text[:1000]  # fallback (safe)

#     # Load model only once
#     if _summarizer is None:
#         print("🧠 Loading summarizer model (one-time)...")
#         _summarizer = pipeline(
#             "summarization",
#             model="facebook/bart-large-cnn"
#         )

#     # BART cannot handle very long input safely
#     safe_text = text[:3000]

#     try:
#         summary = _summarizer(
#             safe_text,
#             max_length=130,
#             min_length=30,
#             do_sample=False
#         )
#         return summary[0]["summary_text"]

#     except Exception as e:
#         print(f"⚠ Summarization skipped: {e}")
#         return text[:1000]
from config import ENABLE_SUMMARY

# Try importing transformers safely (cloud-safe)
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

_summarizer = None


def summarize_text(text):
    global _summarizer

    if not text:
        return ""

    # Feature toggle OR missing dependency
    if not ENABLE_SUMMARY or not TRANSFORMERS_AVAILABLE:
        return text[:1000]  # safe fallback

    # Load model only once
    if _summarizer is None:
        print("🧠 Loading summarizer model (one-time)...")
        _summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )

    # BART cannot handle very long input safely
    safe_text = text[:3000]

    try:
        summary = _summarizer(
            safe_text,
            max_length=130,
            min_length=30,
            do_sample=False
        )
        return summary[0]["summary_text"]

    except Exception as e:
        print(f"⚠ Summarization skipped: {e}")
        return text[:1000]
