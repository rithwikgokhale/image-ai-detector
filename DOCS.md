# Documentation

This project uses Sphinx for professional documentation hosted on Netlify.

## Local Development

```bash
# Install documentation dependencies
pip install -r requirements-docs.txt

# Build documentation
cd sphinx-docs
python3 -m sphinx -b html . _build/html

# View locally
open _build/html/index.html
```

## Netlify Deployment

The documentation automatically deploys to Netlify when pushed to the main branch:

1. **Build Command**: `pip install -r requirements-docs.txt && cd sphinx-docs && python3 -m sphinx -b html . _build/html`
2. **Publish Directory**: `sphinx-docs/_build/html`
3. **Python Version**: 3.9

## Documentation Structure

```
sphinx-docs/
├── index.rst                 # Main landing page
├── conf.py                   # Sphinx configuration
├── user-guide/               # User documentation
│   ├── installation.rst
│   ├── quick-start.rst
│   └── troubleshooting.rst
├── technical/                # Technical documentation
│   ├── architecture.rst
│   ├── ml-approach.rst
│   └── api-reference.rst
├── development/              # Developer documentation
│   └── contributing.rst
├── resources/                # Additional resources
│   ├── faq.rst
│   └── roadmap.rst
└── _static/                  # Static assets
    └── custom.css
```

## Features

- **Modern Theme**: Furo theme with custom branding
- **Interactive Elements**: Tabs, code blocks with copy buttons
- **Responsive Design**: Mobile-friendly layout
- **Search**: Full-text search functionality
- **Cross-references**: Automatic linking between documents
- **Syntax Highlighting**: Code blocks with language detection

## Writing Documentation

- Use reStructuredText (.rst) format
- Follow existing structure and conventions
- Include code examples and screenshots where helpful
- Test locally before committing
- Keep content up-to-date with code changes
