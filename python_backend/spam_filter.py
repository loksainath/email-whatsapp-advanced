# SPAM_KEYWORDS = [
#     "unsubscribe",
#     "resume your learning",
#     "offer",
#     "sale",
#     "discount",
#     "promotion",
#     "marketing",
#     "newsletter",
#     "no-reply",
#     "do not reply",
#     "click here",
#     "buy now"
# ]

# MARKETING_SENDERS = [
#     "simplilearn",
#     "udemy",
#     "coursera",
#     "byjus",
#     "noreply",
#     "marketing"
# ]


# def is_spam(email_body: str, sender: str = "") -> bool:
#     body = email_body.lower()
#     sender = sender.lower()

#     if any(word in body for word in SPAM_KEYWORDS):
#         return True

#     if any(s in sender for s in MARKETING_SENDERS):
#         return True

#     return False

SPAM_KEYWORDS = [
    "unsubscribe",
    "buy now",
    "limited offer",
    "discount",
    "sale",
    "promotion",
    "marketing",
    "newsletter",
    "click here",
    "free trial",
    "enroll now"
]

MARKETING_SENDERS = [
    "noreply",
    "no-reply",
    "marketing",
    "mailer",
    "newsletter",
    "offers"
]

# Always allow emails from these domains / keywords
WHITELIST_SENDERS = [
    "gmail.com",
    "outlook.com",
    "edu",
    "ac.in",
    "mlrit",
    "prof",
    "sir",
    "madam"
]


def is_spam(email_body: str, sender: str = "", subject: str = "") -> bool:
    """
    Returns True if email is likely spam.
    Uses whitelist + keyword scoring.
    """

    body = (email_body or "").lower()
    sender = (sender or "").lower()
    subject = (subject or "").lower()

    # ✅ Whitelist check (highest priority)
    if any(w in sender for w in WHITELIST_SENDERS):
        return False

    spam_score = 0

    # 🚫 Strong spam signals
    if any(s in sender for s in MARKETING_SENDERS):
        spam_score += 2

    # ⚠️ Soft spam signals
    spam_score += sum(1 for w in SPAM_KEYWORDS if w in body)
    spam_score += sum(1 for w in SPAM_KEYWORDS if w in subject)

    # 🎯 Threshold
    return spam_score >= 2

