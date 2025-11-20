def extract_title(markdown: str) -> str:
    # Enforcing that headers should be double newline separated from other content
    blocks = markdown.split("\n\n")
    title = ""
    for block in blocks:
        if block[0:2] == "# ":
            title = block[2:]
            break
    if title == "":
        raise Exception("No title found")

    return title
