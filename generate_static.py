"""Flask web application to render the dataset homepage."""

import os
import shutil
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template

app = Flask(__name__)


def generate_static_html():
    """Render the dataset homepage."""
    # Dataset information
    authors, affiliations = read_authors_from_tsv()

    # Create author string for citation from the authors list
    author_names = [author["name"] for author in authors]
    author_citation = ", ".join(author_names)

    dataset_info = {
        "title": "From smartphones to satellites: Uniting crowdsourced biodiversity monitoring and Earth observation to fill the gaps in global plant trait mapping",
        "authors": authors,
        "affiliations": affiliations,
        "buttons": [
            {
                "text": "Preprint",
                "alt": "Read the paper",
                "icon": "file-alt",
                "link": "http://dx.doi.org/10.1101/2025.03.10.641660",
            },
            {
                "text": "Data Viewer",
                "alt": "View the dataset",
                "icon": "earth-america",
                "link": "https://global-traits.projects.earthengine.app/view/global-traits",
            },
            {
                "text": "Download",
                "alt": "Download the dataset",
                # "icon": "database",
                "icon": "download",
                "link": "https://zenodo.org/records/14646322",
            },
            {
                "text": "GitHub",
                "alt": "View the source code",
                "icon": "code-branch",
                "link": "https://github.com/GeoSense-Freiburg/cit-sci-traits",
            },
        ],
        "image_title": "31 functional traits at 1 km resolution",
        "sample_image": "static/images/exemplar.png",
        "image_caption": "Global mean plant height in meters at 1 km resolution presented in Equal Area Scalable Earth (EASE) projection.",
        "abstract": """
        Plant functional traits are fundamental to ecosystem dynamics and Earth system processes, but their global characterization is limited by the availability of field surveys and trait measurements. Recent expansions in biodiversity data aggregation, including large collections of vegetation surveys, citizen science observations, and trait measurements, offer new opportunities to overcome these constraints. Here we demonstrate that combining these diverse data sources with high-resolution Earth observation data enables accurate modeling of key plant traits at up to 1 km resolution. Our approach achieves high predictive power, reaching correlations up to 0.63 (15 of 31 traits exceeding 0.50) and improved spatial transferability, effectively bridging gaps in under-sampled regions. By capturing a broad range of traits with high spatial coverage, these maps can enhance our understanding of plant community properties and ecosystem functioning globally, and can serve as useful tools in modeling global biogeochemical processes and informing worldwide conservation efforts. Ultimately, our framework highlights the power and necessity of crowdsourced biodiversity data in high-resolution plant trait modeling. We anticipate that advancements in biodiversity data collection and remote sensing capabilities will further refine global trait mapping, fostering a dynamic trait-based understanding of the biosphere.
        """,
        "methodology": """
        Vegetation occurrences from citizen science sources (CIT) and vegetation plot surveys (SCI) were matched with mean trait values by species name with trait databases. This served to produce three training data sets (CIT, SCI, and a combination of the two) used to extrapolate community-level trait values as a function of environmental and Earth observation data. Ensemble gradient-boosting was used for trait modeling.
        <br><br>
        Earth observation datasets used as predictors include: MODIS surface reflectance, SoilGrids2.0 soil properties, WorldClim Bioclimatic variables, and the Vegetation Optical Depth Climate Archive (VODCA).
        """,
        "methodology_image": "static/images/methodology.png",
        "usage_notes": """
        Here you can find maps of 31 plant functional traits as defined in the <a href="https://www.try-db.org/" target="_blank" alt=TRY Plant Trait Database>TRY Plant Trait Database</a> with a resolution of 1 km and a global extent. The maps are extrapolations by ensemble models trained on ~40 million citizen science species observations from the <a href="https://www.gbif.org/" target="_blank" alt=Global Biodiversity Information Facility">Global Biodiversity Information Facility</a> as well as scientific species abundances recorded in the <a href="https://www.idiv.de/en/splot.html" target="_blank" alt="sPlot">sPlot</a> database in combination with TRY trait data and global Earth observation datasets.
        <br>
        <br>
        The current iteration of the trait maps includes traits sourced from plants across three major plant functional types (PFTs): shrubs, trees, and grasses. PFT-specific maps are in progress and will be available soon.
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
        @dataset{lusk_global_2025,
            title = {Global plant trait maps based on crowdsourced biodiversity monitoring and Earth observation - 1 km - All {PFTs}},
            url = {https://zenodo.org/records/14646322},
            doi = {10.5281/zenodo.14646322},
            abstract = {Global, high-resolution plant trait maps based on crowdsourced biodiversity monitoring and Earth observation},
            version = {1.0.0},
            publisher = {Zenodo},
            author = {Lusk, Daniel and Wolf, Sophie and Svidzinska, Daria and Kattenborn, Teja},
            urldate = {2025-03-11},
            date = {2025-03-10},
            keywords = {1-km, Citizen science, Earth observation, Functional ecology, Global maps, notion, Plant traits},
            file = {Snapshot:/home/daniel/Zotero/storage/R396Z8PR/14646322.html:text/html},
        }""",
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


def read_authors_from_tsv():
    """Read author and affiliation information from the TSV file using pandas."""
    from pathlib import Path

    import pandas as pd

    authors = []
    affiliations = {}
    affiliation_map = {}  # Maps affiliation name to ID
    affiliation_counter = 1

    tsv_path = Path("./static/authors.tsv")

    # Read TSV file using pandas
    df = pd.read_csv(tsv_path, sep="\t", encoding="utf-8")

    for _, row in df.iterrows():
        # Extract information
        email = row["Email"]
        first_name = row["First Name"]
        middle_name = (
            row.get("Middle Name(s)/Initial(s)", "")
            if "Middle Name(s)/Initial(s)" in df.columns
            else ""
        )
        middle_name = str(middle_name).strip() if not pd.isna(middle_name) else ""
        last_name = row["Last Name"]
        orcid = row.get("ORCiD", "") if "ORCiD" in df.columns else ""
        orcid = str(orcid).strip() if not pd.isna(orcid) else ""
        affiliation1 = str(row["Affiliation 1"]).strip()
        affiliation2 = (
            row.get("Affiliation 2", "") if "Affiliation 2" in df.columns else ""
        )
        affiliation2 = str(affiliation2).strip() if not pd.isna(affiliation2) else ""
        link = row["Link"] if not pd.isna(row["Link"]) else ""

        # Construct full name
        full_name = first_name
        if middle_name:
            full_name += f" {middle_name}"
        full_name += f" {last_name}"

        # Process affiliations
        author_affiliations = []

        # Handle first affiliation
        if affiliation1:
            if affiliation1 not in affiliation_map:
                affiliation_map[affiliation1] = affiliation_counter
                affiliations[affiliation_counter] = affiliation1
                affiliation_counter += 1
            author_affiliations.append(str(affiliation_map[affiliation1]))

        # Handle second affiliation if present
        if affiliation2:
            if affiliation2 not in affiliation_map:
                affiliation_map[affiliation2] = affiliation_counter
                affiliations[affiliation_counter] = affiliation2
                affiliation_counter += 1
            author_affiliations.append(str(affiliation_map[affiliation2]))

        # Combine affiliations with comma
        affiliation_str = ",".join(author_affiliations)
        # if len(author_affiliations) > 1:
        #     # Add quotes if multiple affiliations (for display purposes)
        #     affiliation_str = f'{affiliation_str}"'

        # Create author entry
        # Use email domain to guess a link if needed
        # email_domain = email.split("@")[1] if "@" in email else ""
        # link = ""

        # if "uni-freiburg.de" in email_domain:
        #     link = f"https://uni-freiburg.de/profile/{email.split('@')[0]}"
        # elif "idiv" in email_domain:
        #     link = f"https://www.idiv.de/en/profile/{last_name.lower()}.html"
        # elif "bgc-jena" in email_domain or "mpg" in email_domain:
        #     link = f"https://www.bgc-jena.mpg.de/person/{last_name.lower()}"
        # else:
        #     # Default to ResearchGate as fallback
        #     link = f"https://www.researchgate.net/profile/{first_name}-{last_name}"

        author = {
            "name": full_name,
            "affiliation": affiliation_str,
            "link": link,
            "orcid": orcid if orcid else "",
        }

        authors.append(author)

    return authors, affiliations


if __name__ == "__main__":
    generate_static_html()
