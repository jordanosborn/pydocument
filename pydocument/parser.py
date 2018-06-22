"""Document parser."""
import re
from collections import OrderedDict
from pydocument.document import doc
import pydocument.utils as utils
import pydocument.generators as generators
from typing import Callable

KEYWORDS = [
    'DATE',
    'NUMBER',
    'NAME',
    'EVAL',
    'CURRENCY',
    'ADDRESS',
    'CODE',
    'TEXT'
]

USER_KEYWORDS = []

FUNCTIONS = {key: None for key in KEYWORDS}

FUNCTIONS['RECALL'] = generators.builtin.recall

USER_FUNCTIONS = {}

KEYWORD_MODIFIERS = [
    'p'
]

OPERATORS = {
    'arithmetic': {
        '+',
        '-',
        '/',
        '*',
        '%'
    },
    'comparison': {
        'neq': '!=',
        'eq': '==',
        'lt': '<',
        'gt': '>',
        'lte': ['<=', '=<'],
        'gte': ['>=', '=>'],
        'mlt': '<<',
        'mgt': '>>',
        'and': 'and',
        'or': 'or',
        'not': 'not'
    },
    'assignment': {
        '=',
    },
    'control': {
        'if': 'IF',
        'else': 'ELSE',
        'elseif': 'ELSEIF',
        'for': 'FOR',
        'while': 'WHILE'
    }
}

INTERNAL_VARIABLE_KEY = '_'


def create_keyword(keyword: str, function: Callable[[str], str]) -> None:
    """Create a keyword by passing in a keyword and a generator function.

    Arguments:
        keyword {str} -- keyword to create
        function {Callable[[str]]} -- function that generates a value

    """
    if keyword not in KEYWORDS and keyword not in USER_KEYWORDS:
        USER_KEYWORDS.append(keyword)
        USER_FUNCTIONS[keyword] = function
    elif keyword in KEYWORDS:
        print(f"Can't redefine the built in keyword: {keyword}.")
    elif keyword in USER_KEYWORDS:
        print(f"Redifining the user defined keyword: {keyword}.")
        USER_FUNCTIONS[keyword] = function


def find_function(keyword: str) -> Callable[[str], str]:
    """Find generator function for keyword.

    Arguments:
        keyword {str} -- keyword

    Returns:
        Callable[[str], str] -- generator function for keyword

    """
    if keyword in FUNCTIONS.keys():
        return FUNCTIONS[keyword]
    elif keyword in USER_FUNCTIONS.keys():
        return USER_FUNCTIONS[keyword]
    elif keyword == 'RECALL':
        return lambda x: ''
    else:
        return lambda x: ''


class parser:
    """DOCUMENT PARSER CLASS."""

    def __init__(self, filetype: str) -> None:
        """Initialise a document parser.

        Arguments:
            filetype {string} -- type of parser to initialise.
        """
        self.parser_type = filetype
        self.id = ['${', '}']
        # TODO: Matches variable groups in raw text. Doesn't allow \} in var.
        # [<]([w][:][\w])[ ]+?([\w\s\S]*?)[>]([\w\s\S]*?)([<][\/](\1)?[>])$
        # Matches word tag pairs
        self.variable_regex = re.compile(r"(?<!\\)([$][{][^}]*[}]{1})")
        if self.parser_type == 'docx':
            self.parse = self._parse_docx
            self.render = self._render_docx
            # Captures anything of form </w:ahths> or <w:tgagas agsga>
            # TODO: (non-ideal)
            self.word_tag_capture = re.compile(
                r"([<][w][:][\w\s\S]*?[>]|[<][\/][w][:][\w]*?[>])")
            # TODO: Look for non-matching ${

    def _parse_variable_text(self, variable_text: str) -> dict:
        """Parse variable text that has been embedded in a document.

        Arguments:
            variable_text {str} -- input variable text.

        Returns:
            str -- parsed variable.

        """
        parsed = ''
        for n in self.word_tag_capture.finditer(variable_text):
                parsed += n.group(1)
                variable_text = variable_text.replace(n.group(1), '')
        # TODO: Error handling of variable text. Non unique name invalid format
        parsed = variable_text + parsed

        parsed_text = variable_text[len(self.id[0]): -len(self.id[1])].strip()

        args = []
        modifiers = []
        name = ''

        # Split string into expression and its arguments.
        parsed_text_split = utils.strings.split_string(parsed_text, ',')
        if len(parsed_text_split) > 1:
            args = parsed_text_split[1:]
        parsed_text_split = utils.strings.strip_list(parsed_text_split[0].split())
        # Find type
        keyword = ''
        for word in KEYWORDS + USER_KEYWORDS:
            for modifier in KEYWORD_MODIFIERS:
                if parsed_text_split[0] == word:
                    keyword = word
                    break
                elif parsed_text_split[0] == modifier + word:
                    keyword = word
                    modifiers.append(modifier)
                    break

        if keyword == '':
            if len(parsed_text_split) == 1:
                keyword = 'RECALL'
                name = parsed_text_split[0]
            else:
                raise ValueError(f'\nUnrecognisable variable string\n\t{variable_text}.\n')
        # TODO: be careful with unnamed variables, unique name and
        else:
            if len(parsed_text_split) > 1 and keyword != 'EVAL':
                name = parsed_text_split[1]

        if name != '' and name[0] == INTERNAL_VARIABLE_KEY:
            raise ValueError(
                f'\nInvalid variable name {name}. Variables can\'t start with {INTERNAL_VARIABLE_KEY}.' +
                f'\n\t{variable_text}\n'
            )

        return {
            'type': keyword,
            'name': name,
            'text': variable_text,
            'operator': '',
            'expression': '',
            'args': args,
            'parsed': parsed,
            'modifiers': modifiers
        }

    def _parse_docx(self, content: doc) -> OrderedDict:
        """Parse document and restructure its content.

        Arguments:
            content {doc} -- file content to parse

        Returns:
            variables {dict} -- dict of var name and value pairs.

        """
        variables = OrderedDict()

        if content.filetype == 'docx':
            # TODO: other files contain text information
            text = str(content.raw['word/document.xml'], 'utf-8')
            for m in self.variable_regex.finditer(text):
                pos = m.start()
                unparsed = m.group(1)
                try:
                    parsed_variable_text = self._parse_variable_text(unparsed)
                except ValueError as e:
                    print(e)
                else:
                    if parsed_variable_text['name'] not in variables.keys() or parsed_variable_text['type'] == 'RECALL':
                        variables[parsed_variable_text['name']] = {
                            'type': parsed_variable_text['type'],
                            'text': parsed_variable_text['text'],
                            'operator': parsed_variable_text['operator'],
                            'expression': parsed_variable_text['expression'],
                            'args': parsed_variable_text['args'],
                            'position': pos,
                            'modifiers': parsed_variable_text['modifiers'],
                            'function': find_function(parsed_variable_text['type'])
                        }
                        parsed = parsed_variable_text['parsed']
                        # TODO: need variable versions so can have different arguments for recalled variables.
                        text = text.replace(unparsed, parsed).replace(
                            parsed_variable_text['text'],
                            self.id[0] + parsed_variable_text['name'] + self.id[1]
                        )
                    else:
                        print(
                            f'\nRedifinition of variable {parsed_variable_text["name"]}',
                            f'\n\t{variables[parsed_variable_text["name"]]["text"]}',
                            f'at {variables[parsed_variable_text["name"]]["position"]}.',
                            f'\n\t{parsed_variable_text["text"]}',
                            f' at {pos}.\n'
                        )
            content.raw['word/document.xml'] = text.encode()
            return variables
        else:
            print('Invalid file passed to Docx parser.')
            return OrderedDict()

    def _render_docx(self, content: str, context: dict) -> str:
        """Render document based on context.

        Arguments:
            content {str} -- the document to modify
            context {dict} -- variable and value key pairs.

        Returns:
            str -- rendered document.

        """
        return ''
