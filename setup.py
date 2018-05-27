from setuptools import setup

setup(
    name='pydocument',
    version='0.0.1',
    description='a pip-installable package',
    license='MIT',
    packages=['pydocument'],
    author='Jordan Osborn',
    author_email='jordanosborn0@gmail.com',
    keywords=['example'],
	install_requires=[
          'pypandoc',
		  'pdfminer.six'
      ],
    url='https://github.com/jordanosborn/pydocument'
)