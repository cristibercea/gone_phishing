import re

def validate_url(input_string: str) -> None:
    """
    Validates that the given string is considered a URL.
    :param input_string: the string to validate
    :raises AttributeError: if the string is not a URL
    :return: None
    """
    url_regex = re.compile(r"^https?://.*$")
    if not url_regex.match(input_string): raise AttributeError(f'\'{input_string}\' is not a valid URL!')