# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys


project = "aiida-fans"
copyright = "2024-%Y, Ethan Shanahan"
author = "Ethan Shanahan"
sys.path.append("../../src/")
from aiida_fans._version import version as version
from aiida_fans._version import version as release

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = []

master_doc = "index"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_favicon = "_static/aiida-fans-logo.png"
html_logo = "_static/aiida-fans-logo.png"
html_title = "aiida-fans"
html_last_updated_fmt = ""
html_static_path = ["_static"]

html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_url": "https://github.com/ethan-shanahan/aiida-fans",
    "use_repository_button": True,
}

