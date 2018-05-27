from io import BytesIO, StringIO
from zipfile import ZipFile

class doc:
	import mimetypes
	import magic
	import pypandoc
	from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
	from pdfminer.pdfpage import PDFPage
	from pdfminer.converter import HTMLConverter, TextConverter
	from pdfminer.layout import LAParams
	from io import BytesIO

	number = 0
	def __init__(self, filepath):
		doc.number += 1
		mime = doc.magic.Magic(mime=True)
		self.filepath = filepath
		try:
			self.mimetype = mime.from_file(self.filepath)
			self.filetype = doc.mimetypes.guess_extension(self.mimetype)[1:]
		except FileNotFoundError:
			print("File not found!")
			del self
		self.filename = self.filepath.split('/')[-1].split('.')[0]

	def _get(self, variable):
		if variable == 'mimetype':
			print(self.mimetype)
		elif variable == 'filetype':
			print(self.filetype)
	def search(self, terms, replacements = [], output = ''):
		if len(replacements)==len(terms) != 0:
			for i in range(0,len(terms)):
				replaced_text = self.text.replace(terms[i], replacements[i])
			self.save(replaced_text, output)
		else:
			for term in terms:
				print(self.text.find(term))
	def save(self, text, output):
		file_format = output.split('.')[-1]
		open('temp.html','wb').write(text)
		out = doc.pypandoc.convert_file('temp.html', file_format, format='html')
		open(output, 'w').write(out)
		
	
	def open(self):
		def _openDOCX():
			file = BytesIO(open(self.filepath, 'rb').read())
			zipfile_ob = ZipFile(file)
			#substructure of document
			self.raw = {name: zipfile_ob.read(name) for name in zipfile_ob.namelist()}
			self.text = doc.pypandoc.convert_file(self.filepath, 'html', format=self.filetype, extra_args='--extract-media ./' + self.filename )
			open("test.html",'w').write(self.text)
				
		def _openXLSX():
			file = BytesIO(open(self.filepath, 'rb').read())
			zipfile_ob = ZipFile(file)
			#substructure of document
			self.raw = {name: zipfile_ob.read(name) for name in zipfile_ob.namelist()}
		#use lib/pdftohtml instead?
		def _openPDF():
			out_type = 'html'
			rsrcmgr = doc.PDFResourceManager()
			sio = doc.BytesIO()
			codec = 'utf-8'
			laparams = doc.LAParams()
			converter = doc.TextConverter if out_type=='text' else doc.HTMLConverter
			device = converter(rsrcmgr, sio, codec='utf-8', laparams=laparams)
			interpreter = doc.PDFPageInterpreter(rsrcmgr, device)

			fp = open(self.filepath, 'rb')
			for page in doc.PDFPage.get_pages(fp, check_extractable=False):
				interpreter.process_page(page)
			self.raw = fp.read()
			fp.close()

			# Get text from StringIO
			self.text = sio.getvalue()

			# Cleanup
			device.close()
			sio.close()


		if self.filetype == 'docx':
			_openDOCX()
		elif self.filetype == 'pdf':
			_openPDF()
		elif self.filetype == 'xlsx':
			_openXLSX
	
	def close(self):
		doc.number -= 1
