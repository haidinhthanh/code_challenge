import time
from os import path
from collections import defaultdict
from constant.path import LOG_PATH
from utils.logUtils import LogAction
from utils.fileUtils import read_lines_text_file
from utils.stringUtils import *
from asset.punctuation_mark import PUNCTUATION_MARK
import logging
from argparse import ArgumentParser


def main():
    arg_parser = ArgumentParser('word_counter.py -p path -t type')
    arg_parser.add_argument('-p', '--path', default=None, help='Ban nho nhap duong dan tuyet doi cua file text ')
    arg_parser.add_argument('-t', '--type', default=None, help='Ban nho nhap loai sap xep [asc, desc] ')
    args = arg_parser.parse_args()
    file_path = args.path
    sort_type = args.type
    if not sort_type:
        sort_type = "desc"
    word_counter = WordCounter()
    dictionary = word_counter.cal_word_frequency_in_doc(document_path=file_path,
                                                        arrange_type=sort_type)
    print("Result: \n")
    print("{\n")
    for key, value in dictionary.items():
        print("word: {word}; num of word: {freq} \n".format(word=key, freq=value))
    print("\n}")


class WordCounter:
    def __init__(self, mode=""):
        self.log = LogAction(name=__file__).init_log(path_folder_logs=path.join(LOG_PATH, "count_log"))
        if mode == "test":
            logging.disable(logging.INFO)

    def pre_process_before_count(self, document_lines):
        start_time = time.time()
        normalize_lines = list()
        for line in document_lines:
            line = lower_sentence(line)
            date_match_objects, replace_line = find_date_entity_by_pattern(line)
            time_match_objects, replace_line = find_url_entity_by_pattern(replace_line)
            replace_line = add_space_to_unwanted_char(replace_line)
            normalize_line = convert_entity_in_sen_to_normal(replace_line, date_match_objects + time_match_objects)
            normalize_lines.append(normalize_line)

        normalize_document = "\n".join(normalize_lines)
        self.log.info("Duration pre process before count: {duration}".format(duration=float(time.time() - start_time)))
        return normalize_document

    def word_count(self, document):
        start_time = time.time()
        dictionary = dict()
        counter = defaultdict(int)
        for line in document.splitlines():
            for word in line.split():
                if word not in PUNCTUATION_MARK:
                    counter[word] += 1
        for word, cnt in sorted(counter.items(), key=lambda x: (-x[1], x[0])):
            dictionary[word] = cnt
        self.log.info("Duration count dictionary: {duration}".format(duration=float(time.time() - start_time)))
        return dictionary

    def cal_word_frequency_in_doc(self, document_path, arrange_type="desc"):

        document_lines = read_lines_text_file(document_path)
        document = self.pre_process_before_count(document_lines)

        desc_dictionary = self.word_count(document)
        if arrange_type == "asc":
            asc_dictionary = dict()
            for word, cnt in sorted(desc_dictionary.items(), key=lambda x: (x[1], x[0])):
                asc_dictionary[word] = cnt
            return asc_dictionary
        elif arrange_type == "desc":
            return desc_dictionary
        else:
            self.log.info("Not valid arrange type")
            return None

