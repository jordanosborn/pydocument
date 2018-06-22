"""Compile source."""

import os
from fnmatch import fnmatch
from distutils.core import setup, Extension
from Cython.Build import cythonize

root = './'
pattern = "*.py"
sourcefiles = []

for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name, pattern) and name not in ['setup.py', 'compile.py']:
            sourcefiles.append(os.path.join(path, name))

ext_files = []
for s in sourcefiles:
    ext_files.append(Extension(s[2:].replace('.py', '').replace('/', '.'), [s]))
    print(s[2:].replace('.py', '').replace('/', '.'))

setup(
     name='pydocument',
     ext_modules=cythonize(ext_files)
)
