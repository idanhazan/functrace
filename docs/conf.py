import os
import sys

sys.path.insert(0, os.path.abspath('..'))

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
# autodoc_class_signature = 'separated'
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
