SPAM_KEYWORDS = [
    "unsubscribe",
    "resume your learning",
    "offer",
    "sale",
    "discount",
    "promotion",
    "marketing",
    "newsletter",
    "no-reply",
    "do not reply",
    "click here",
    "buy now"
]

MARKETING_SENDERS = [
    "simplilearn",
    "udemy",
    "coursera",
    "byjus",
    "noreply",
    "marketing"
]


def is_spam(email_body: str, sender: str = "") -> bool:
    body = email_body.lower()
    sender = sender.lower()

    if any(word in body for word in SPAM_KEYWORDS):
        return True

    if any(s in sender for s in MARKETING_SENDERS):
        return True

    return False
