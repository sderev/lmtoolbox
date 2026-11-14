from strip_tags.lib import strip_tags


def extract_text(html: str) -> str:
    """Exclude parsed template elements when extracting webpage text."""
    return strip_tags(input=html, minify=True, removes=["template"])
