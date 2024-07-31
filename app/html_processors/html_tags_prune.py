from bs4 import Tag

TAGS_TO_REMOVE = ["script", "form", "img", "svg", "path", "button"]


def prune_html_tags(html: Tag, tags_to_remove: list[str] = TAGS_TO_REMOVE) -> Tag:
    # Remove specified tags
    for tag in tags_to_remove:
        for element in html.find_all(name=tag):
            element.decompose()  # Remove the element from the soup
    return html
