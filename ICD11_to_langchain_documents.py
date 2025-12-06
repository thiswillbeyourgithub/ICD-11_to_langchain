# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
#     "click",
#     "langchain_core",
# ]
# ///

"""Script to load a file into a pandas DataFrame and open a breakpoint.

This script takes a file path as an argument, loads it into a pandas DataFrame,
and then opens a Python debugger breakpoint for interactive exploration.

Created with assistance from aider.chat.
"""

import pickle
import re

import click
import pandas as pd
from langchain_core.documents import Document


version = "0.1.0"


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option(
    "--language",
    default="fr",
    help="Language for titles: 'fr' (default) or 'en'. Crashes for other values.",
)
@click.option(
    "--remove_unused_metadata",
    is_flag=True,
    default=True,
    help="Remove metadata fields with pd.isna values (default: True).",
)
@click.option(
    "--output",
    default=f"ICD-11-v{version}.pickle",
    type=click.Path(),
    help=f"Output path for pickled documents (default: ICD-11-v{version}.pickle).",
)
@click.option(
    "--strip-bullets",
    is_flag=True,
    default=True,
    help="Remove leading '- ' from page_content (default: True).",
)
def main(
    filepath: str,
    language: str,
    remove_unused_metadata: bool,
    output: str,
    strip_bullets: bool,
) -> None:
    """Load a file into a pandas DataFrame and create langchain Documents.

    Parameters
    ----------
    filepath : str
        Path to the file to load into a DataFrame.
    language : str
        Language for titles: 'fr' for French (default) or 'en' for English.
        The script will crash if any other value is provided.
    remove_unused_metadata : bool
        If True, remove metadata fields where pd.isna(value) is True.
    output : str
        Path where the pickled list of langchain Documents will be saved.
    strip_bullets : bool
        If True, remove all leading "- " prefixes from page_content.
        This handles cases where multiple "- " prefixes are present.

    Notes
    -----
    The file is loaded as tab-separated values (TSV) by default, which matches
    the ICD-11 MMS format. This can be adjusted if needed for other file formats.
    """
    # Validate language parameter
    # Only 'fr' and 'en' are supported to ensure correct title column selection
    if language not in ["fr", "en"]:
        raise ValueError(f"Language must be 'fr' or 'en', got '{language}'")

    # Determine which title column to use based on language
    # French uses 'Title', English uses 'TitleEN'
    title_column = "Title" if language == "fr" else "TitleEN"
    # Load the file into a DataFrame
    # Using tab separator to match the ICD-11 MMS SimpleTabulation format
    df = pd.read_csv(filepath, sep="\t")

    # Clean BrowserLink column to extract only the URL
    # The column contains Excel-style hyperlink formulas in the format:
    # =hyperlink("https://...", "browser")
    # We extract just the URL portion to make the links directly usable
    if "BrowserLink" in df.columns:

        def extract_url(link: str) -> str:
            """Extract URL from Excel hyperlink formula.

            Parameters
            ----------
            link : str
                Excel hyperlink formula string.

            Returns
            -------
            str
                Extracted URL, or original value if no match found.
            """
            if pd.isna(link):
                return link
            match = re.search(r'=hyperlink\("(.+?)","', link)
            if match:
                return match.group(1)
            return link

        df["BrowserLink"] = df["BrowserLink"].apply(extract_url)

    # Build a dictionary mapping chapter numbers to chapter titles
    # This allows us to look up chapter titles for blocks
    # Uses the appropriate title column based on selected language
    chapter_titles = {}
    for _, row in df.iterrows():
        if row["ClassKind"] == "chapter":
            chapter_titles[row["ChapterNo"]] = row[title_column]

    # Add ChapterTitle column for blocks
    # For each block row, look up the chapter title using its ChapterNo
    df["ChapterTitle"] = ""
    for idx, row in df.iterrows():
        if row["ClassKind"] in ["block", "category"]:
            chapter_no = row["ChapterNo"]
            df.at[idx, "ChapterTitle"] = chapter_titles.get(chapter_no, "")

    # Convert each row into a langchain Document
    # page_content contains the title and chapter title for context
    # metadata contains all row data for filtering and reference
    documents = []
    for _, row in df.iterrows():
        page_content = f"{row[title_column]} ({row['ChapterTitle']})"

        # Strip leading bullets if requested
        # This removes all leading "- " prefixes that may be present
        if strip_bullets:
            while page_content.startswith("- "):
                page_content = page_content[2:]

        metadata = row.to_dict()

        # Remove unused metadata fields if requested
        # This cleans up the metadata by removing fields with pd.isna values
        if remove_unused_metadata:
            metadata = {k: v for k, v in metadata.items() if not pd.isna(v)}

        doc = Document(page_content=page_content, metadata=metadata)
        documents.append(doc)

    # Pickle the documents to the output file
    # This allows the documents to be loaded and used in other scripts
    with open(output, "wb") as f:
        pickle.dump(documents, f)

    click.echo(f"Successfully saved {len(documents)} documents to {output}")


if __name__ == "__main__":
    main()
