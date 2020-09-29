def read_text_file(path):
    """
    Read text content from file path
    :param path: str
        Input file path
    :return: str
        Content text input
    """
    with open(path, "r", encoding="utf8") as file:
        document = file.read()
    return document


def read_lines_text_file(path):
    """
    Read list of lines in text file input
    :param path: str
        Input file path
    :return: list
        List of lines in text file input
    """
    with open(path, "r", encoding="utf8") as file:
        document = file.readlines()
    return document
