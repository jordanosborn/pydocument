"""Document parser."""
import re
from collections import OrderedDict
from pydocument.document import doc

KEYWORDS: list = [
    'DATE',
    'NUMBER',
    'NAME',
    'EVAL',
    'MONEY',
    'ADDRESS',
    'CODE',

]


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
        print(parsed)
        return {
            'type': '',
            'name': '',
            'text': variable_text,
            'operator': '',
            'expression': '',
            'args': '',
            'parsed': parsed
        }

    def _parse_docx(self, content: doc) -> OrderedDict:
        """Parse document and restructure its content.

        Arguments:
            content {doc} -- file content to parse

        Returns:
            variables {dict} -- dict of var name and value pairs.

        """
        variables: OrderedDict = OrderedDict()

        if content.filetype == 'docx':
            # TODO: other files contain text information
            text = str(content.raw['word/document.xml'], 'utf-8')
            for m in self.variable_regex.finditer(text):
                pos = m.start()
                unparsed = m.group(1)
                parsed_variable_text = self._parse_variable_text(unparsed)
                # TODO: Name conflict unless type == recall
                variables[parsed_variable_text['name']] = {
                    'type': parsed_variable_text['type'],
                    'text': parsed_variable_text['text'],
                    'operator': parsed_variable_text['operator'],
                    'expression': parsed_variable_text['expression'],
                    'args': parsed_variable_text['args'],
                    'position': pos
                }
                parsed = parsed_variable_text['parsed']
                text = text.replace(unparsed, parsed).replace(
                    parsed_variable_text['text'],
                    self.id[0] + parsed_variable_text['name'] + self.id[1]
                )
            content.raw['word/document.xml'] = text.encode()
        return variables

    def _render_docx(self, content: str, context: dict) -> str:
        """Render document based on context.

        Arguments:
            content {str} -- the document to modify
            context {dict} -- variable and value key pairs.

        Returns:
            str -- rendered document.

        """
        return ''
