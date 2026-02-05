# Global Plant Trait Maps Website

Static website generator for a scientific research dataset publication page.

## Tech Stack

- **Python 3.12+** with Flask and Jinja2 templating
- **Package manager:** uv
- **Styling:** Dark theme with Fira Sans / DM Serif Text fonts

## Project Structure

```
templates/index.html    # Main Jinja2 template
static/
  style.css             # Site styling
  authors.tsv           # Author metadata (tab-separated)
  images/               # PNG/PDF assets
docs/                   # Generated output (GitHub Pages)
generate_static.py      # Build script
```

## Commands

```bash
# Install dependencies
uv sync

# Build static site (outputs to docs/)
python generate_static.py
```

## Workflow

1. Edit `templates/index.html` or `static/` files
2. Run `python generate_static.py` to rebuild
3. Commit changes including `docs/` folder
4. GitHub Pages serves from `docs/`

## Author Data

Authors are defined in `static/authors.tsv` with columns: name, institution, orcid, is_corresponding
