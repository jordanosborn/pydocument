"""Templater class."""

from copy import deepcopy
from pydocument.document import doc
from pydocument.parser import parser
import json
from collections import OrderedDict

from multiprocessing.dummy import Pool

class templater:
    """Template class."""

    def __init__(self, template: doc, settings: str, output_folder: str, naming_convention: tuple) -> None:
        """[summary]

        Arguments:
            template {doc} -- document that needs templating
            settings {str} -- settings file path
            output_folder {str} -- output folder directory
            naming_convention {tuple} -- convention to name files (prefix, suffix)

        Returns:
            None -- no return value

        """

        self.template = deepcopy(template)
        with open(settings, 'r') as f:
            self.settings = json.loads(f.read())

        self.output_folder = output_folder
        self.naming_convention = naming_convention
        self.parser = parser(template.get('filetype'))

    def _save_context(self, outputt: str) -> None:
        """Save the currently generated context.

        Arguments:
            output {str} -- output file.

        Returns:
            None -- no return value
        """
        pass

    def generate(self, number: int = -1) -> None:
        """Generate documents.

        Keyword Arguments:
            number {int} -- number to generate leave blank if constructing from data (default: {-1})

        Returns:
            None -- no return value

        """
        self.variables = self.parser.parse(self.template)
        print(self.variables)
