from bs4 import BeautifulSoup

TAGS_MAPPING: dict[str, str] = {
    "h1": "#",
    "h2": "#",
    "h3": "#",
    "h4": "#",
    "h5": "#",
    "h6": "#",
    "p": "",
    "li": "*",
}


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
    for element in soup.find_all(name=TAGS_MAPPING.keys()):
        if element.name.startswith("h"):
            level = int(element.name[1])  # Get header level
            texts.append(
                "\n"
                + TAGS_MAPPING[element.name] * level
                + " "
                + element.get_text(strip=True)
                + "\n"
            )
        elif element.name == "p":
            texts.append("\n" + element.get_text(strip=True) + "\n")
        elif element.name == "li":
            texts.append(
                TAGS_MAPPING[element.name] + " " + element.get_text(strip=True) + "\n"
            )
    return "".join(texts)
