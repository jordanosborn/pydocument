"""Manages different document types."""
from io import BytesIO
from zipfile import ZipFile

import mimetypes
import magic
import pypandoc
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import HTMLConverter, TextConverter
from pdfminer.layout import LAParams


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
        try:
            self.mimetype = mime.from_file(self.filepath)
            self.filetype = str(mimetypes.guess_extension(self.mimetype))[1:]
            self.filename = filepath.split('/')[-1].split('.')[0]
            if self.filetype == 'docx':
                self._openDOCX()
            elif self.filetype == 'pdf':
                self._openPDF()
            elif self.filetype == 'xlsx':
                self._openXLSX()
        except FileNotFoundError:
            print("File not found!")
            self.close()

    def _get(self, variable: str) -> None:
        if variable == 'mimetype':
            print(self.mimetype)
        elif variable == 'filetype':
            print(self.filetype)

    def replace(self, context: dict = {}, output: str = '') -> None:
        """Replace key/value pairs in document.

        Keyword Arguments:
            context {dict} -- search/replace pairs. (default: {[]})
            output {str} -- filename to save output as. (default: {''})

        Returns:
            None -- [description]

        """
        if len(context) != 0:
            for key in context.keys():
                replaced_text = self.text.replace(key, context[key])
            self.save(replaced_text, output)

    def save(self, text: str, output: str) -> None:
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
            pass
        else:
            pass

    def convert(self, output: str) -> None:
        """Convert file into different format.

        Arguments:
            output (str): [description]

        Returns:
            None: has no return value.

        """
        self.text = pypandoc.convert_file(
            self.filepath,
            'html5',
            format=self.filetype,
            extra_args='--extract-media ./' + output
        )

    def _openDOCX(self) -> None:
        """Open docx file and store its contents."""
        with open(self.filepath, 'rb') as f:
            file = BytesIO(f.read())
        zipfile_ob = ZipFile(file)
        # substructure of document
        self.raw = {
            name: zipfile_ob.read(name) for name in zipfile_ob.namelist()
        }

    def _openXLSX(self) -> None:
        """Open excel file and store its contents."""
        with open(self.filepath, 'rb') as f:
            file = BytesIO(f.read())
        zipfile_ob = ZipFile(file)
        # substructure of document
        self.raw = {
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
        self.raw = {'document.pdf': fp.read()}
        fp.close()

        # Get text from BytesIO
        self.text = sio.getvalue()

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
