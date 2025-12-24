# from bs4 import BeautifulSoup
# import re


# def clean_email_body(raw_html: str) -> str:
#     if not raw_html:
#         return ""

#     # Parse HTML
#     soup = BeautifulSoup(raw_html, "lxml")

#     # Remove scripts, styles, tracking
#     for tag in soup(["script", "style", "img", "svg", "noscript"]):
#         tag.decompose()

#     text = soup.get_text(separator=" ")

#     # Normalize spaces
#     text = re.sub(r"\s+", " ", text)
#     text = text.strip()

#     return text

# from bs4 import BeautifulSoup
# import re


# def clean_email_body(raw_html) -> str:
#     """
#     Safely clean email HTML/text for cloud deployment.
#     Handles None, plain text, and HTML emails.
#     """

#     if raw_html is None:
#         return ""

#     # Ensure input is string
#     raw_html = str(raw_html)

#     # Parse HTML using built-in parser (no lxml dependency)
#     soup = BeautifulSoup(raw_html, "html.parser")

#     # Remove unwanted tags
#     for tag in soup(["script", "style", "img", "svg", "noscript"]):
#         tag.decompose()

#     # Extract visible text
#     text = soup.get_text(separator=" ")

#     # Normalize whitespace
#     text = re.sub(r"\s+", " ", text).strip()

#     return text


import re
from html import unescape


def clean_email_body(html: str, max_chars: int = 3500) -> str:
    """
    Converts HTML email to clean WhatsApp-safe text.
    - Removes tags
    - Removes tracking links
    - Collapses whitespace
    - Enforces WhatsApp length limit
    """

    if not html:
        return ""

    # Remove script/style
    html = re.sub(r"<(script|style).*?>.*?</\1>", "", html, flags=re.S | re.I)

    # Remove all HTML tags
    text = re.sub(r"<[^>]+>", " ", html)

    # Decode HTML entities
    text = unescape(text)

    # Remove URLs (optional but recommended)
    text = re.sub(r"https?://\S+", "", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Enforce WhatsApp limit
    if len(text) > max_chars:
        text = text[:max_chars] + " …(truncated)"

    return text
