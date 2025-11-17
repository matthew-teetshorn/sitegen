from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(string: str) -> list[str]:
    strings = string.split("\n\n")

    strings = [substring.strip() for substring in strings]

    remove = ""
    strings = [keep for keep in strings if keep != remove]

    return strings


def block_is_heading(block: str) -> bool:
    # Supported heading style 1-6 '#' with <space> after
    REGEX_H = r"^\#{1,6}\s"

    # Currently only support headings on single lines with newlines surrounding
    if "\n" in block or re.findall(REGEX_H, block) == []:
        return False

    return True


def block_is_code(block: str) -> bool:
    # Supported code block style ``` stuff ```
    REGEX_C = r"^`{3}.*`{3}$"

    # Code blocks can contain newline sequences
    if re.findall(REGEX_C, block, flags=re.DOTALL) == []:
        return False

    return True


def block_is_quote(block: str) -> bool:
    # Supported quote symbol: > with <space> after
    REGEX_Q = r"^\> "

    substrings = block.split("\n")
    for substring in substrings:
        if re.search(REGEX_Q, substring) is None:
            return False

    return True


def block_is_ul(block: str) -> bool:
    # Supported unordered list symbol: '-' with <space> after
    REGEX_UL = r"^\- "

    substrings = block.split("\n")
    for substring in substrings:
        if re.search(REGEX_UL, substring) is None:
            return False

    return True


def block_is_ol(block: str) -> bool:
    # Supported ordered list symbol: 'N' with <space> after
    # N must start at '1' and increment by 1 on each substring
    REGEX_OL = r"^(\d+)\. "

    substrings = block.split("\n")
    start_num = 1
    for substring in substrings:
        regex_result = re.findall(REGEX_OL, substring)
        if regex_result == [] or int(regex_result[0]) != start_num:
            return False
        start_num += 1

    return True


def block_to_blocktype(block: str) -> BlockType:
    if block_is_heading(block):
        return BlockType.HEADING
    if block_is_code(block):
        return BlockType.CODE
    if block_is_quote(block):
        return BlockType.QUOTE
    if block_is_ul(block):
        return BlockType.UNORDERED_LIST
    if block_is_ol(block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
