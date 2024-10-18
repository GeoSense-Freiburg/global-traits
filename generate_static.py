"""Flask web application to render the dataset homepage."""

import os
from pathlib import Path
import shutil
from flask import Flask, render_template

app = Flask(__name__)


def generate_static_html():
    """Render the dataset homepage."""
    # Dataset information
    dataset_info = {
        "title": "Global, high-resolution plant trait maps combining citizen science and Earth observation",
        "authors": [
            {"name": "Daniel Lusk", "affiliation": 1},
            {"name": "Teja Kattenborn", "affiliation": 1},
        ],
        "affiliations": {
            1: "Sensor-based Geoinformatics, University of Freiburg",
            2: "Institute of AI Research",
        },
        "paper_link": "https://example.com/dataset-paper",
        "app_link": "https://example.com/view-dataset-app",
        "data_link": "https://example.com/download-dataset",
        "code_link": "https://github.com/username/dataset-source-code",
        "sample_image": "static/images/sample_image.jpg",
        "image_caption": "Sample image from the dataset.",
        "abstract": "This dataset contains ... [your dataset abstract here].",
        "methodology": "We collected data using ... [methodology details].",
        "citation": """
        @misc{doe2024dataset,
          author = {John Doe and Jane Smith},
          title = {My Amazing Dataset},
          year = {2024},
          howpublished = {\\url{https://github.com/username/dataset-repo}},
        }
        """,
        "related_work": [
            {"title": "Related Work 1", "link": "https://example.com/related1"},
            {"title": "Related Work 2", "link": "https://example.com/related2"},
        ],
    }

    with app.app_context():
        html_content = render_template("index.html", dataset=dataset_info)

        # Define the output directory for static HTML (GitHub Pages uses /docs)
        output_dir = Path("docs")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Write the rendered HTML to index.html in the /docs directory
        with open(output_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        # Copy the static folder (CSS, images, etc.) to the /docs directory
        static_src_dir = Path(os.getcwd(),  "static")
        static_dest_dir = output_dir / "static"

        if static_dest_dir.exists():
            shutil.rmtree(static_dest_dir)  # Clean out the old static folder

        shutil.copytree(static_src_dir, static_dest_dir)

        print(f"Static site generated at: {output_dir}/index.html")


if __name__ == "__main__":
    generate_static_html()
