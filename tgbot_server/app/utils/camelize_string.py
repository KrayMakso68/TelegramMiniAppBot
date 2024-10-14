def camelize(string: str) -> str:
    """
    Convert string to camelCase. camelCase starts with a lower case alphabetic character, the rest of the string
    contains alphanumeric characters. Any character case in the input is ignored. Any spaces in the input capitalise
    the following character if alphabetic, except for the first character. Any non-alphanumeric characters are ignored.

    :param string: The input string.
    :return: The input converted to camelCase; empty ('') if there are no valid characters in the input string.
    :raises: AssertionError if the input is not of type str.
    """

    assert isinstance(string, str), 'Input must be of type str'

    first_alphabetic_character_index = -1
    for index, character in enumerate(string):
        if character.isalpha():
            first_alphabetic_character_index = index
            break

    empty = ''

    if first_alphabetic_character_index == -1:
        return empty

    string = string[first_alphabetic_character_index:]

    titled_string_generator = (character for character in string.title() if character.isalnum())

    try:
        return next(titled_string_generator).lower() + empty.join(titled_string_generator)

    except StopIteration:
        return empty
