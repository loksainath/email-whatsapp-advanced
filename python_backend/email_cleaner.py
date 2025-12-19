from bs4 import BeautifulSoup
import re


def clean_email_body(raw_html: str) -> str:
    if not raw_html:
        return ""

    # Parse HTML
    soup = BeautifulSoup(raw_html, "lxml")

    # Remove scripts, styles, tracking
    for tag in soup(["script", "style", "img", "svg", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    # Normalize spaces
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text
