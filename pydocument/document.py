"""Manages different document types."""
from io import BytesIO
from zipfile import ZipFile
# from __future__ import annotations
from typing import Dict, List, Any

import mimetypes
import magic
import pypandoc
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from bs4 import BeautifulSoup

import pydocument.utils as utils


class doc:
    """Document class.

    Handles different document types
    """

    number = 0

    def __init__(self, filepath: str) -> None:
        """Initialise document.

        Arguments:
            filepath {str} -- path to file.

        Returns:
            None -- has no return value.

        """
        doc.number += 1
        mime = magic.Magic(mime=True)
        self.filepath = filepath

        # TODO: not ideal
        if filepath != '':
            try:
                self.mimetype = mime.from_file(self.filepath)
            except FileNotFoundError:
                print("File not found!")
                self.close()
            else:
                self.filetype = str(mimetypes.guess_extension(self.mimetype))[1:]
                self.filename = filepath.split('/')[-1].split('.')[0]
                if self.filetype == 'docx':
                    self._openDOCX()
                elif self.filetype == 'pdf':
                    self._openPDF()
                elif self.filetype == 'xlsx':
                    self._openXLSX()
                else:
                    # TODO: unknown file type path etc.
                    pass

    # TODO: when python3.7 alter any to doc.
    @classmethod
    def from_raw(cls, filename: str, filetype: str, raw_content: Dict[str, bytes]) -> Any:
        """Create document object from raw.

        Arguments:
            filename {str} -- name of file
            filetype {str} -- type of file
            raw_content {dict[str, BytesIO]} -- dict of file structure

        Returns:
            None -- no return value

        """
        a = cls('')
        a.filename = filename
        a.filetype = filetype
        a.__raw = raw_content
        # TODO: _extract_text method
        a.text = str(raw_content[list(raw_content.keys())[0]])
        return a

    def __str__(self) -> str:
        """Return string version of document.

        Returns:
            {str} -- str form of document

        """
        return self.text

    def get(self, variable: str) -> None:
        if variable == 'mimetype':
            return self.mimetype
        elif variable == 'filetype':
            return self.filetype

    @property
    def raw(self) -> Dict[str, bytes]:
        """Return raw file contents.

        Returns:
            Dict[str, bytes] -- file contents.

        """
        return self.__raw

    def replace(self, context: dict = {}, output: str = '') -> None:
        """Replace key/value pairs in document.

        Keyword Arguments:
            context {dict} -- search/replace pairs. (default: {[]})
            output {str} -- filename to save output as. (default: {''})

        Returns:
            None -- [description]

        """
        # TODO: is broken currently.
        if len(context) != 0:
            for key in context.keys():
                replaced_text = ''.replace(key, context[key])
            self.save(output)

    def save(self, output: str) -> None:
        """Save document in format.

        Arguments:
            text {str} -- text to save.
            output {str} -- file to output.

        Returns:
            None -- has no return value.

        """
        # Handle file types here docx etc.
        filetype = output.split('.')[-1]
        if filetype == self.filetype:
            if self.filetype == 'docx':
                zip_file = ZipFile(output, "w")
                for key, value in self.raw.items():
                    zip_file.writestr(key, value)
                zip_file.close()

        else:
            pass

    def convert(self, filetype: str) -> None:
        """Convert file into different format.

        Arguments:
            filetype (str): output filetype

        Returns:
            None: has no return value.

        """
        text = pypandoc.convert_file(
            self.filepath,
            filetype,
            format=self.filetype,
            # extra_args='--extract-media ./' + output
        )
        return text

    def _extract_text(self) -> None:
        """Extract text from raw file.

        Returns:
            None -- has no return value.

        """
        if self.filetype == 'docx':
            soup = BeautifulSoup(self.__raw['word/document.xml'], "xml")
            self.paragraphs = soup.findAll('w:p')
            for i, p in enumerate(self.paragraphs):
                soup = BeautifulSoup(str(p), 'xml')
                self.paragraphs[i] = soup.get_text()
            self.text = utils.strings.join_all(self.paragraphs, '\n')

    def _openDOCX(self) -> None:
        """Open docx file and store its contents."""
        with open(self.filepath, 'rb') as f:
            file = BytesIO(f.read())
        zipfile_ob = ZipFile(file)
        # substructure of document
        self.__raw = {
            name: zipfile_ob.read(name) for name in zipfile_ob.namelist()
        }
        # Split by W:P tags and get text
        self._extract_text()

    def _openXLSX(self) -> None:
        """Open excel file and store its contents."""
        with open(self.filepath, 'rb') as f:
            file = BytesIO(f.read())
        zipfile_ob = ZipFile(file)
        # substructure of document
        self.__raw = {
            name: zipfile_ob.read(name) for name in zipfile_ob.namelist()
        }
    # use lib/pdftohtml instead?

    def _openPDF(self) -> None:
        """Open pdf file and store its contents."""
        out_type = 'html'
        rsrcmgr = PDFResourceManager()
        sio = BytesIO()
        codec = 'utf-8'
        laparams = LAParams()
        converter = TextConverter if out_type == 'text' else HTMLConverter
        device = converter(rsrcmgr, sio, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        fp = open(self.filepath, 'rb')
        for page in PDFPage.get_pages(fp, check_extractable=False):
            interpreter.process_page(page)
        self.__raw = {'document.pdf': fp.read()}
        fp.close()

        # Get text from BytesIO
        # text = sio.getvalue()

        # Cleanup
        device.close()
        sio.close()

    def close(self) -> None:
        """Close file.

        Returns:
            None: has no return value

        """
        doc.number -= 1
        del self
