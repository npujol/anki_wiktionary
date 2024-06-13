from bs4 import BeautifulSoup


def extract_ordered_text(raw_html: str) -> str:
    """
    Extracts ordered text from HTML.

    Args:
        raw_html (str): The raw HTML content.

    Returns:
        str: The extracted text.

    """
    soup = BeautifulSoup(markup=raw_html, features="html.parser")
    texts = []
    for element in soup.find_all(name=["h1", "h2", "h3", "h4", "h5", "h6", "p", "li"]):
        if element.name.startswith("h"):
            level = int(element.name[1])  # Get header level
            texts.append("\n" + "#" * level + " " + element.get_text(strip=True) + "\n")
        elif element.name == "p":
            texts.append("\n" + element.get_text(strip=True) + "\n")
        elif element.name == "li":
            texts.append("* " + element.get_text(strip=True) + "\n")
    return "".join(texts)
