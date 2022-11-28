import re


def detect_dash(input_text: str):
    pattern = re.compile(r".*-")
    return pattern.match(input_text)


def detect_alphabet(input_text: str):
    pattern = re.compile(r"\d\d[a-zA-Z]")
    return pattern.match(input_text)
