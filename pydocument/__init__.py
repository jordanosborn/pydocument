from pydocument.pydocument import *

from pypandoc import get_pandoc_version
if not get_pandoc_version():
	pypandoc.pandoc_download()
del get_pandoc_version