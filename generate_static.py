"""Flask web application to render the dataset homepage."""

import os
from pathlib import Path
import shutil
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


def generate_static_html():
    """Render the dataset homepage."""
    # Dataset information
    dataset_info = {
        "title": "Global, high-resolution plant trait maps combining citizen science and Earth observation",
        "authors": [
            {
                "name": "Daniel Lusk",
                "affiliation": 1,
                "link": "https://uni-freiburg.de/enr-geosense/team/daniel_lusk/",
                "orcid": "0009-0002-9745-5011",
            },
            {
                "name": "Sophie Wolf",
                "affiliation": 2,
                "link": "https://www.uni-leipzig.de/en/profile/mitarbeiter/sophie-wolf",
                "orcid": "0000-0001-7848-3725",
            },
            {
                "name": "Daria Svidzinska",
                "affiliation": 2,
                "link": "https://www.researchgate.net/profile/Daria-Svidzinska",
                "orcid": "0000-0002-1578-6312",
            },
            {
                "name": "Jens Kattge",
                "affiliation": "3,4",
                "link": "https://www.bgc-jena.mpg.de/person/jkattge/4965278",
                "orcid": "0000-0002-1022-8469",
            },
            {
                "name": "Francesco Maria Sabatini",
                "affiliation": "3,5,6",
                "link": "https://www.unibo.it/sitoweb/francescomaria.sabatini/en",
                "orcid": "0000-0002-7202-7697",
            },
            {
                "name": "Álvaro Moreno Martínez",
                "affiliation": 7,
                "link": "https://www.researchgate.net/profile/Alvaro-Moreno-2",
                "orcid": "0000-0003-2990-7768",
            },
            {
                "name": "Teja Kattenborn",
                "affiliation": 1,
                "link": "https://uni-freiburg.de/enr-geosense/team/kattenborn/",
                "orcid": "0000-0001-7381-3828",
            },
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
        "buttons": [
            # {
            #     "text": "Paper",
            #     "alt": "Read the paper",
            #     "icon": "file-alt",
            #     "link": "https://example.com/dataset-paper",
            # },
            # {
            #     "text": "App",
            #     "alt": "View the dataset",
            #     "icon": "earth-europe",
            #     "link": "https://example.com/view-dataset-app",
            # },
            {
                "text": "Download",
                "alt": "Download the dataset",
                # "icon": "database",
                "icon": "download",
                "link": "https://kattenborn.go.bwsfs.uni-freiburg.de:11443/web/client/pubshares/2pxZ92URZ2jMdAuCxereHf/browse",
            },
            # {
            #     "text": "Code",
            #     "alt": "View the source code",
            #     "icon": "code-branch",
            #     "link": "https://github.com/username/dataset-source-code",
            # },
        ],
        "image_title": "33 functional traits at 1 km resolution",
        "sample_image": "static/images/exemplar.png",
        "image_caption": "Global mean plant height in meters at 0.01° (~1 km) resolution presented in Equal Earth projection.",
        "abstract": """
        The acceleration of global environmental change underscores the pressing need for a comprehensive understanding of how the biosphere interacts with its environment. To reliably examine these connections across diverse ecosystems, having spatially continuous data on plant functional traits is imperative. Trait databases such as TRY boast an extensive repository of plant trait measurements for thousands of species for individual locations. Previous approaches have attempted to spatially extrapolate such local trait measurements using environmental predictors or Earth observation data. Thereby, a common challenge is the scarcity of the original data, which leads to significant uncertainty in the extrapolations in data-scarce regions. Meanwhile, rapidly growing citizen science initiatives, such as iNaturalist or Pl@ntNet, have generated millions of ground-level species observations across the globe. Despite being noisy and opportunistically sampled, previous studies have shown that integrating such citizen science species observations with large functional trait databases enables the creation of global trait maps with unprecedented accuracy. However, aggregating citizen science data only allows for the generation of sparse and relatively coarse trait maps, e.g. at 0.2 to 2.0 degree spatial resolution.
        <br><br>
        Here, by using such citizen science data in concert with high-resolution Earth observation data, we extend this approach to model the relationships between functional traits and their structural and environmental determinants, providing global trait maps with globally continuous coverage and unprecedented spatial resolution (up to 1km). This fusion of ground-based citizen science and continuous satellite data allows us not only to map more 20 ecologically relevant traits but also to derive crucial functional diversity metrics at a global scale. These metrics—such as functional richness and evenness—provide new opportunities to explore the role of functional diversity in ecosystem stability, particularly in response to climate extremes associated with climate change. Our approach presents a scalable framework to advance understanding of plant functional traits and diversity, opening the door to new insights on how ecosystems may respond to an increasingly variable and extreme climate.
        """,
        "methodology": "Crowd-sourced vegetation occurrences from GBIF (which species observations from contains popular citizen science initiatives such as iNaturalist and Pl@ntNet, among many others) and curated plot-level species abundances from sPlot were matched with mean species trait values from the TRY Trait Database. Ensemble gradient-boosting models were trained for each trait as a function of environmental and Earth observation data.<br><br>The Earth observation data used in this experiment were: MODIS surface reflectance, SoilGrids2.0 soil properties, WorldClim Bioclimatic variables, and the Vegetation Optical Depth Climate Archive (VODCA).",
        "methodology_image": "static/images/methodology.png",
        "usage_notes": """
        Here you can find maps of 33 plant functional traits as defined in the <a href="https://www.try-db.org/" target="_blank" alt=TRY Plant Trait Database>TRY Plant Trait Database</a> with a resolution of 0.01°°(~1.1 km at the equator) and a global extent. The maps are extrapolations by ensemble models trained on ~40 million citizen science species observations from the <a href="https://www.gbif.org/" target="_blank" alt=Global Biodiversity Information Facility">Global Biodiversity Information Facility</a> as well as scientific species abundances recorded in the <a href="https://www.idiv.de/en/splot.html" target="_blank" alt="sPlot">sPlot</a> database in combination with TRY trait data and global Earth observation datasets.
        <br>
        <br>
        The current iteration of the trait maps includes traits sourced from plants across three major plant functional types (PFTs): shrubs, trees, and grasses. PFT-specific maps are in progress and will be available in the future.
        <br>
        <br>
        For questions, please contact Daniel Lusk (<a href="mailto:daniel.lusk@geosense.uni-freiburg.de">daniel.lusk [at] geosense.uni-freiburg.de</a>).

        """,
        "citation": """
        @misc{doe2024dataset,
          author = {John Doe and Jane Smith},
          title = {My Amazing Dataset},
          year = {2024},
          howpublished = {\\url{https://github.com/username/dataset-repo}}
        }
        """,
        "related_work": [
            {"title": "TRY Trait Database", "link": "https://www.try-db.org/"},
            {
                "title": "Global Biodiversity Information Facility",
                "link": "https://www.gbif.org/",
            },
            {"title": "sPlot", "link": "https://www.idiv.de/en/splot.html"},
        ],
        "current_year": datetime.now().year,
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
        static_src_dir = Path(os.getcwd(), "static")
        static_dest_dir = output_dir / "static"

        if static_dest_dir.exists():
            shutil.rmtree(static_dest_dir)  # Clean out the old static folder

        shutil.copytree(static_src_dir, static_dest_dir)

        print(f"Static site generated at: {output_dir}/index.html")


if __name__ == "__main__":
    generate_static_html()
