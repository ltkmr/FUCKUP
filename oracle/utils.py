def gematria_value(text):
    """
    Calculates a simple gematria value for a given string.
    A=1, B=2, ..., Z=26. Case-insensitive. Non-letters are ignored.
    """
    value = 0
    for char in text.upper():
        if char.isalpha():
            value += ord(char) - ord('A') + 1
    return value