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
            # {
            #     "name": "Francesco Maria Sabatini",
            #     "affiliation": "3,5,6",
            #     "link": "https://www.unibo.it/sitoweb/francescomaria.sabatini/en",
            #     "orcid": "0000-0002-7202-7697",
            # },
            # {
            #     "name": "Helge Bruelheide",
            #     "affiliation": "6",
            #     "link": "https://www.botanik.uni-halle.de/geobotanik/helge_bruelheide/",
            #     "orcid": "0000-0003-3135-0356",
            # },
            # {
            #     "name": "Gabriella Damasceno",
            #     "affiliation": "3,6",
            #     "link": "https://www.idiv.de/en/profile/1716.html",
            #     "orcid": "0000-0001-5103-484X",
            # },
            # {
            #     "name": "Álvaro Moreno Martínez",
            #     "affiliation": 7,
            #     "link": "https://www.researchgate.net/profile/Alvaro-Moreno-2",
            #     "orcid": "0000-0003-2990-7768",
            # },
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
        Plant functional traits describe the form and function of plant communities and are vital to understanding the mechanics of the terrestrial biosphere, yet knowledge of their global distribution remains limited to specific regions and geographically restricted datasets. Meanwhile, rapidly growing citizen science initiatives have generated hundreds of millions of ground-level species observations across the globe. While previous studies have shown the integration of citizen science observations with large functional trait databases can enable the creation of global trait maps with promising accuracy, citizen science data alone remains insufficient to facilitate trait mapping at high resolutions due to noise caused by opportunistic collection practices. Recently curated aggregations of professional vegetation surveys offer higher-quality observations, but are comparatively few in number. Fortunately, large Earth observation datasets present an opportunity to help bridge these gaps due to their high resolution and global coverage. Here, we combine the multivariate strengths of citizen science, vegetation surveys, and Earth observation data to model the relationships between functional traits and their structural and environmental determinants, yielding continuous global trait maps of over 30 ecologically-relevant plant traits with unprecedented accuracy at high spatial resolution (up to 1 km).
        """,
        "methodology": """
        Vegetation occurrences from citizen science sources (CIT) and vegetation plot surveys (SCI) were matched with mean trait values by species name with trait databases. This served to produce three training data sets (CIT, SCI, and a combination of the two) used to extrapolate community-level trait values as a function of environmental and Earth observation data. Ensemble gradient-boosting was used for trait modeling.
        <br><br>
        Earth observation datasets used as predictors include: MODIS surface reflectance, SoilGrids2.0 soil properties, WorldClim Bioclimatic variables, and the Vegetation Optical Depth Climate Archive (VODCA).
        """,
        "methodology_image": "static/images/methodology.png",
        "usage_notes": """
        Here you can find maps of 33 plant functional traits as defined in the <a href="https://www.try-db.org/" target="_blank" alt=TRY Plant Trait Database>TRY Plant Trait Database</a> with a resolution of 0.01°°(~1.1 km at the equator) and a global extent. The maps are extrapolations by ensemble models trained on ~40 million citizen science species observations from the <a href="https://www.gbif.org/" target="_blank" alt=Global Biodiversity Information Facility">Global Biodiversity Information Facility</a> as well as scientific species abundances recorded in the <a href="https://www.idiv.de/en/splot.html" target="_blank" alt="sPlot">sPlot</a> database in combination with TRY trait data and global Earth observation datasets.
        <br>
        <br>
        The current iteration of the trait maps includes traits sourced from plants across three major plant functional types (PFTs): shrubs, trees, and grasses. PFT-specific maps are in progress and will be available in the future.
        <br>
        <br>
        For questions, please contact Daniel Lusk (<a href="mailto:daniel.lusk@geosense.uni-freiburg.de">daniel.lusk [at] geosense.uni-freiburg.de</a>).
        <br>
        <br>
        These products have been created in the framework of the PANOPS project. More information on this project is available at:
        <ul>
            <li><a href="https://uni-freiburg.de/enr-geosense/research/panops/" target="_blank">https://uni-freiburg.de/enr-geosense/research/panops/</a></li>
            <li><a href="https://gepris-extern.dfg.de/gepris/projekt/504978936?language=en" target="_blank">https://gepris-extern.dfg.de/gepris/projekt/504978936?language=en</a></li>

        """,
        "citation": """
        @dataset{lusk_globaltraits_2025,
          authors = {Daniel Lusk, Sophie Wolf, Daria Svidzinska, Jens Kattge, Teja Kattenborn},
          title = {Global, high-resolution plant trait maps combining citizen science and Earth observation},
          year = {2025},
          howpublished = {\\url{https://kattenborn.go.bwsfs.uni-freiburg.de:11443/web/client/pubshares/2pxZ92URZ2jMdAuCxereHf/browse}}
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
