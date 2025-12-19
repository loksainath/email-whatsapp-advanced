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
from bs4 import BeautifulSoup
import re


def clean_email_body(raw_html) -> str:
    """
    Safely clean email HTML/text for cloud deployment.
    Handles None, plain text, and HTML emails.
    """

    if raw_html is None:
        return ""

    # Ensure input is string
    raw_html = str(raw_html)

    # Parse HTML using built-in parser (no lxml dependency)
    soup = BeautifulSoup(raw_html, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "img", "svg", "noscript"]):
        tag.decompose()

    # Extract visible text
    text = soup.get_text(separator=" ")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text
