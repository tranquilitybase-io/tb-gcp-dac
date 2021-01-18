
def is_none_or_empty(string: str) -> bool:
    if string is None or string == "" or string.isspace():
        return True
    return False
