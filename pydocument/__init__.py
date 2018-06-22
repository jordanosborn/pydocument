"""Pydocument initialisation."""

from pydocument.document import doc
from pydocument.parser import parser

from pypandoc import get_pandoc_version, pandoc_download
if not get_pandoc_version():
    pandoc_download()
del get_pandoc_version, pandoc_download

docx_parser = parser('docx')
pdf_parser = parser('pdf')
