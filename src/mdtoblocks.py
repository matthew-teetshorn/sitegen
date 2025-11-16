def markdown_to_blocks(string: str) -> list[str]:
    strings = string.split("\n\n")

    strings = [substring.strip() for substring in strings]

    remove = ""
    strings = [keep for keep in strings if keep != remove]

    return strings
