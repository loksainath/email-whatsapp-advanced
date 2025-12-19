def classify_priority(subject, body):
    # Safe text handling
    subject = subject or ""
    body = body or ""

    text = f"{subject} {body}".lower()

    if any(word in text for word in [
        "shortlisted", "selected", "offer", "interview",
        "urgent", "internship"
    ]):
        return "HIGH"

    if any(word in text for word in [
        "meeting", "schedule", "exam", "deadline"
    ]):
        return "MEDIUM"

    return "LOW"
