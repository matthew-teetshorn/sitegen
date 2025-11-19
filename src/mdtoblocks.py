from enum import Enum
import regex

import re_defs


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
    # Currently only support headings on single lines with newlines surrounding
    if "\n" in block or regex.findall(re_defs.REGEX_HEADING, block) == []:
        return False

    return True


def block_is_code(block: str) -> bool:
    # Code blocks can contain newline sequences
    if regex.findall(re_defs.REGEX_CODE_BLOCK, block, flags=regex.DOTALL) == []:
        return False

    return True


def block_is_quote(block: str) -> bool:
    substrings = block.split("\n")
    for substring in substrings:
        if regex.search(re_defs.REGEX_BLOCK_QUOTE, substring) is None:
            return False

    return True


def block_is_ul(block: str) -> bool:
    substrings = block.split("\n")
    for substring in substrings:
        if regex.search(re_defs.REGEX_UL_ITEM, substring) is None:
            return False

    return True


def block_is_ol(block: str) -> bool:
    substrings = block.split("\n")
    start_num = 1
    for substring in substrings:
        regex_result = regex.findall(re_defs.REGEX_OL_ITEM, substring)
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
