# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Image AI Detector'
copyright = '2024, Rithwik Gokhale'
author = 'Rithwik Gokhale'
release = '1.0'
version = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.githubpages',
    'myst_parser',
    'sphinx_copybutton',
    'sphinx_tabs.tabs',
]

# MyST Parser configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_title = f"{project} Documentation"

# Furo theme options
html_theme_options = {
    "sidebar_hide_name": True,
    "light_logo": "logo.png",
    "dark_logo": "logo.png",
    "dark_mode_code_blocks": True,
    "light_css_variables": {
        "color-brand-primary": "#2563eb",
        "color-brand-content": "#2563eb",
        "color-admonition-background": "transparent",
    },
    "dark_css_variables": {
        "color-brand-primary": "#2563eb",
        "color-brand-content": "#2563eb",
        "color-background-primary": "#0f172a",
        "color-background-secondary": "#1e293b",
        "color-background-hover": "#334155",
        "color-background-border": "#475569",
        "color-foreground-primary": "#f8fafc",
        "color-foreground-secondary": "#e2e8f0",
        "color-foreground-muted": "#94a3b8",
        "color-foreground-border": "#64748b",
    },
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/rithwikgokhale/image-ai-detector",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}

html_static_path = ['_static']
html_css_files = ['custom.css']

# Copy button configuration
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = True
copybutton_remove_prompts = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'requests': ('https://requests.readthedocs.io/en/latest/', None),
    'flask': ('https://flask.palletsprojects.com/en/2.3.x/', None),
}

# Napoleon settings for Google/NumPy docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# Source file suffixes
source_suffix = {
    '.rst': None,
    '.md': 'myst_parser',
}

# Master document
master_doc = 'index'

# Add any paths that contain custom static files (such as style sheets)
html_favicon = '_static/favicon.ico'

# HTML context for template variables
html_context = {
    "display_github": True,
    "github_user": "rithwikgokhale",
    "github_repo": "image-ai-detector",
    "github_version": "main",
    "conf_py_path": "/sphinx-docs/",
}

# Search language
html_search_language = 'en'

# Show source link
html_show_sourcelink = False

# Show copyright
html_show_copyright = True

# Show sphinx info
html_show_sphinx = False