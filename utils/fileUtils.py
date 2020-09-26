def read_text_file(path):
    with open(path, "r", encoding="utf8") as file:
        document = file.read()
    return document


def read_lines_text_file(path):
    with open(path, "r", encoding="utf8") as file:
        document = file.readlines()
    return document
