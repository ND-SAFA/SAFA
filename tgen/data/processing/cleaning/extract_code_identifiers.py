from typing import List, Tuple

import javac_parser
from comment_parser import comment_parser
from comment_parser.comment_parser import UnsupportedError

from tgen.common.constants.deliminator_constants import NEW_LINE, SPACE
from tgen.common.constants.path_constants import JAVA_KEYWORDS_PATH
from tgen.common.util.logging.logger_manager import logger
from tgen.data.processing.abstract_data_processing_step import AbstractDataProcessingStep


class ExtractCodeIdentifiersStep(AbstractDataProcessingStep):
    """
    Extracts the identifiers in pieces of code including class names, variable names, method names, and code comments.
    """

    def __init__(self):
        """
        Initializes step with code parsers.
        """
        super().__init__()
        self._java = None
        self.java_reserved_words = self.get_java_reserved_words()

    def get_java(self):
        """
        Lazy initializes java object.
        :return:
        """
        if self._java is None:
            self._java = javac_parser.Java()
        return self._java

    def run(self, data_entries: List, **kwargs) -> List:
        """
        If code extracts identifiers, otherwise entries are left untouched.
        :param data_entries: The entries to process.
        :param kwargs: Ignored.
        :return: Processed entries
        """
        return [self.create_class_doc(s) for s in data_entries]

    def create_class_doc(self, class_text: str):
        """
        Extracts the identifiers from the given java class and cleans each identifier.
        Cleaning includes removing non-alphanumeric characters, splitting chained method calls,
        split camel case phrases, and stemming each word.
        :param class_text: A string representing a compiling java class.
        """
        class_doc = self.extract_java_identifiers(class_text)
        return class_doc

    def extract_java_identifiers(self, class_text):
        """
        Returns a string of space-delimited code identifiers from given text
        :param class_text: a string containing some java source code
        :return:
        """
        parsed_syntax_items = self.get_java().lex(class_text)

        def is_java_identifier(syntax_item: Tuple[str, str]):
            """
            Calculates if word is an identifier (e.g. variable name).
            :param syntax_item: Tuple containing label and word.
            :return: True if identifier and not a reserved word.
            """
            word_label = syntax_item[0]
            word = syntax_item[1]
            return word_label == "IDENTIFIER" and word.lower() not in self.java_reserved_words

        identifiers = list(
            map(lambda id: id[-1], filter(is_java_identifier, parsed_syntax_items))
        )
        if len(identifiers) == 0:
            return class_text

        comments = ExtractCodeIdentifiersStep.extract_class_comments(class_text)
        return SPACE.join(identifiers) + SPACE.join(comments)

    @staticmethod
    def extract_class_comments(class_text, mime_type="text/x-java-source"):
        """
        Extracts the class or inline comments in given source file
        :param class_text: the str representation of the source file
        :param mime_type: the type of source file to parse.
        See https://pypi.org/project/comment-parser/ for list of potential mime_types.
        :return: string of comments in class without any comment related syntax
        """
        try:
            comments = comment_parser.extract_comments_from_str(str(class_text), mime_type)
            comments = [c.text().replace(NEW_LINE, ". ") for c in comments]
        except UnsupportedError as e:
            logger.exception(e)
            return class_text

        return comments

    @staticmethod
    def get_java_reserved_words():
        """
        Returns a list of java reserved words or unwanted class identifiers (e.g. Double, String, Integer, etc. wrapper
        classes).
        """
        reserved_keywords_file = open(JAVA_KEYWORDS_PATH, "r")
        words_file_content = reserved_keywords_file.read()
        reserved_keywords_file.close()
        words = map(lambda word: word.strip(), words_file_content.split(NEW_LINE))
        words = filter(lambda word: len(word) != 0, words)
        words = list(words)
        assert len(words) > 0
        return words
