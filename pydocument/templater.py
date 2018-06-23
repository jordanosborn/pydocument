"""Templater class."""

from pydocument.document import doc

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

        self.template = template
        self.settings = settings
        self.output_folder = output_folder
        self.naming_convention = naming_convention

    def generate(self, number: int = -1):
        pass