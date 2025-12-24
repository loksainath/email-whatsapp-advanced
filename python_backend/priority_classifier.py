# def classify_priority(subject, body):
#     # Safe text handling
#     subject = subject or ""
#     body = body or ""

#     text = f"{subject} {body}".lower()

#     if any(word in text for word in [
#         "shortlisted", "selected", "offer", "interview",
#         "urgent", "internship"
#     ]):
#         return "HIGH"

#     if any(word in text for word in [
#         "meeting", "schedule", "exam", "deadline"
#     ]):
#         return "MEDIUM"

#     return "LOW"


from config import ENABLE_PRIORITY_CLASSIFICATION


def classify_priority(subject: str, body: str) -> str:
    """
    Rule-based priority classifier.
    Explainable, fast, and safe.
    """

    if not ENABLE_PRIORITY_CLASSIFICATION:
        return "NORMAL"

    subject = subject or ""
    body = body or ""

    text = f"{subject} {body}".lower()

    high_priority_keywords = [
        "interview",
        "shortlisted",
        "selected",
        "offer letter",
        "joining",
        "congratulations",
        "urgent",
        "internship",
        "appointment",
        "hall ticket",
        "result declared",
    ]

    medium_priority_keywords = [
        "exam",
        "assessment",
        "test",
        "meeting",
        "schedule",
        "deadline",
        "fee",
        "submission",
        "project review",
        "assignment",
    ]

    low_priority_blockers = [
        "sale",
        "discount",
        "promotion",
        "offer ends",
        "newsletter",
        "unsubscribe",
    ]

    # Downgrade marketing-style emails
    if any(word in text for word in low_priority_blockers):
        return "LOW"

    if any(word in text for word in high_priority_keywords):
        return "HIGH"

    if any(word in text for word in medium_priority_keywords):
        return "MEDIUM"

    return "LOW"
