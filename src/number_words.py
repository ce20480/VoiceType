"""
Number word to digit conversion for Claude Code option selection.

Converts spoken numbers like "one", "two", "three" to "1", "2", "3"
which is essential for selecting options in Claude Code menus.
"""

import re

# Mapping of number words to digits (0-20)
NUMBER_MAP = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
    "eleven": "11",
    "twelve": "12",
    "thirteen": "13",
    "fourteen": "14",
    "fifteen": "15",
    "sixteen": "16",
    "seventeen": "17",
    "eighteen": "18",
    "nineteen": "19",
    "twenty": "20",
}

# Common phrases where numbers should be converted
# e.g., "option one" -> "option 1"
OPTION_PATTERNS = [
    r"option\s+",
    r"select\s+",
    r"choice\s+",
    r"number\s+",
    r"item\s+",
]


def convert_number_words(text: str, aggressive: bool = True) -> str:
    """
    Convert spoken number words to digits.

    Args:
        text: Input text with potential number words
        aggressive: If True, convert all standalone number words.
                   If False, only convert in option-selection contexts.

    Returns:
        Text with number words replaced by digits

    Examples:
        >>> convert_number_words("select option one")
        'select option 1'
        >>> convert_number_words("I have two cats")
        'I have 2 cats'
        >>> convert_number_words("the first one is best")
        'the first 1 is best'
    """
    if not text:
        return text

    result = text

    if aggressive:
        # Convert all standalone number words
        words = result.split()
        converted_words = []

        for word in words:
            # Extract the core word without punctuation
            # Keep track of leading/trailing punctuation
            match = re.match(r'^([^\w]*)(\w+)([^\w]*)$', word)
            if match:
                prefix, core, suffix = match.groups()
                lower_core = core.lower()

                if lower_core in NUMBER_MAP:
                    # Preserve case for the replacement if original was capitalized
                    converted_words.append(f"{prefix}{NUMBER_MAP[lower_core]}{suffix}")
                else:
                    converted_words.append(word)
            else:
                converted_words.append(word)

        result = " ".join(converted_words)
    else:
        # Only convert in specific contexts (option selection)
        for pattern in OPTION_PATTERNS:
            for word, digit in NUMBER_MAP.items():
                # Case insensitive replacement after option-like words
                regex = re.compile(f"({pattern})({word})\\b", re.IGNORECASE)
                result = regex.sub(lambda m: f"{m.group(1)}{digit}", result)

    return result


def convert_ordinals(text: str) -> str:
    """
    Convert ordinal words to their numeric form.

    Args:
        text: Input text with potential ordinal words

    Returns:
        Text with ordinals converted (e.g., "first" -> "1st")

    Note: This is optional and not used by default as it may
    not be desired in all contexts.
    """
    ordinals = {
        "first": "1st",
        "second": "2nd",
        "third": "3rd",
        "fourth": "4th",
        "fifth": "5th",
        "sixth": "6th",
        "seventh": "7th",
        "eighth": "8th",
        "ninth": "9th",
        "tenth": "10th",
    }

    result = text
    for word, ordinal in ordinals.items():
        result = re.sub(rf'\b{word}\b', ordinal, result, flags=re.IGNORECASE)

    return result
