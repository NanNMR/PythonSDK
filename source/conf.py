# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'USNAN SDK'
copyright = '2025, Jon Wedell'
author = 'Jon Wedell'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc', # To be able to automatically detect functions/classes/etc and document them
    'sphinx.ext.napoleon', # To support Google and NumPy format docstrings
    #+'sphinx.ext.viewcode', # To enable the user to jump to the source code
    'sphinx.ext.intersphinx' # To enable links to other Sphinx documentation
]

templates_path = ['_templates']
exclude_patterns = []

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None), # The core python docs
    'requests': ('https://requests.readthedocs.io/en/latest/', None), # The requests library
}

python_maximum_signature_line_length = 140

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
