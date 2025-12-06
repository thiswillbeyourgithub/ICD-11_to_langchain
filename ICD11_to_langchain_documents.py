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
    default="ICD-11.pickle",
    type=click.Path(),
    help="Output path for pickled documents (default: ICD-11.pickle).",
)
def main(
    filepath: str, language: str, remove_unused_metadata: bool, output: str
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
