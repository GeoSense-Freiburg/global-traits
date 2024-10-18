"""Flask web application to render the dataset homepage."""

import os
from pathlib import Path
from re import M
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
            {"name": "Sophie Wolf", "affiliation": 2},
            {"name": "Daria Svidzinska", "affiliation": 2},
            {"name": "Jens Kattge", "affiliation": "3,4"},
            {"name": "Francesco Maria Sabatini", "affiliation": "3,5,6"},
            {"name": "Álvaro Moreno Martínez", "affiliation": 7},
            {"name": "Teja Kattenborn", "affiliation": 1},
        ],
        "affiliations": {
            1: "Sensor-based Geoinformatics, University of Freiburg, Germany",
            2: "Remote Sensing Centre for Earth System Research, Leipzig University, Germany",
            3: "German Centre for Integrative Biodiversity Research (iDiv) Halle-Jena-Leipzig, Germany",
            4: "Max Planck Institute for Biogeochemistry, Germany",
            5: "Department of Biological, Geological and Environmental Sciences (BiGeA), Alma Mater Studiorum University of Bologna, Italy",
            6: "Institute of Biology/Geobotany and Botanical Garden, Martin Luther University Halle-Wittenberg, Germany",
            7: "Image Signal Processing Group, Image Processing Laboratory (IPL), University of Valencia, Spain",
        },
        "paper_link": "https://example.com/dataset-paper",
        "app_link": "https://example.com/view-dataset-app",
        "data_link": "https://example.com/download-dataset",
        "code_link": "https://github.com/username/dataset-source-code",
        "image_title": "33 functional traits at 1 km resolution",
        "sample_image": "static/images/exemplar.png",
        "image_caption": "Global mean plant height in meters at 0.01° (~1 km) resolution presented in Equal Earth projection.",
        "abstract": "Functional diversity has been recognized as a key driver of ecosystem resilience and resistance, yet our understanding of global patterns of functional diversity is constrained to specific regions or geographically limited datasets. Meanwhile, rapidly growing citizen science initiatives, such as iNaturalist or Pl@ntNet, have generated millions of ground-level species observations across the globe. Despite being noisy and opportunistically sampled, previous studies have shown that integrating such citizen science species observations with large functional trait databases enables the creation of global trait maps with unprecedented accuracy. However, aggregating citizen science data allows for the generation of sparse and relatively coarse trait maps, e.g. at 0.2 to 2.0 degree spatial resolution. Here, by using such citizen science data in concert with high-resolution Earth observation data, we extend this approach to model the relationships between functional traits and their structural and environmental determinants, providing global trait maps with globally continuous coverage and unprecedented spatial resolution (up to 1km). This fusion of ground-based citizen science and continuous satellite data allows us not only to map more 20 ecologically relevant traits but also to derive crucial functional diversity metrics at a global scale. These metrics—such as functional richness and evenness—provide new opportunities to explore the role of functional diversity in ecosystem stability, particularly in response to climate extremes associated with climate change. Our approach presents a scalable framework to advance understanding of plant functional traits and diversity, opening the door to new insights on how ecosystems may respond to an increasingly variable and extreme climate.",
        "methodology": "We collected data using ... [methodology details].",
        "citation": """
        @misc{doe2024dataset,
          author = {John Doe and Jane Smith},
          title = {My Amazing Dataset},
          year = {2024},
          howpublished = {\\url{https://github.com/username/dataset-repo}}
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
