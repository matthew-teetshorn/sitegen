# Regular expression definitions
REGEX_HEADING = r"^\#{1,6}\s"
REGEX_CODE_BLOCK = r"^`{3}([^`]+)`{3}$"
REGEX_BLOCK_QUOTE = r"^\>\s*"
REGEX_UL_ITEM = r"^\- "
REGEX_OL_ITEM = r"^(\d+)\. "
REGEX_LINK_FRONT = r"(?<!!)\[([^\[\]]+)\]\("
REGEX_LINK_URL = r"\(((?:[^()]|(?R))*)\)"
REGEX_MARKDOWN_IMG = r'!\[([^[\]]+)\]\(([^"()\s{}<>|\\`[\]]+)\)'
REGEX_BREAK_ENDING = r"\s{2,}\n"
