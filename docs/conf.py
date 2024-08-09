from __future__ import annotations

from os.path import abspath
from sys import path

path.insert(0, abspath('..'))

import functrace

project = 'functrace'
author = 'Idan Hazan'
copyright = f'2024, {author}'
html_theme = 'sphinx_rtd_theme'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]
autodoc_typehints = 'description'
