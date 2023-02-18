# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath('..'))


project = 'python-multiplayer'
copyright = '2023, BroCodeAT'
author = 'BroCodeAT'
release = '0.1.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "numpydoc", "sphinx.ext.viewcode", "autoapi.extension"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Numpydoc configuration --------------------------------------------------

autodoc_typehints = "none"  # NumpyDoc will do it for us. We just want to remove them from the signature too
autodoc_preserve_defaults = True

# -- AutoAPI configuration ---------------------------------------------------

autoapi_root = "reference"
autoapi_dirs = ["../src"]
autoapi_ignore = ["__main__.py"]

autoapi_options = ["members", "show-inheritance"]
autoapi_template_dir = "_templates"

autoapi_add_toctree_entry = False
autoapi_add_objects_to_toctree = False
autoapi_keep_files = True
autoapi_member_order = "groupwise"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
