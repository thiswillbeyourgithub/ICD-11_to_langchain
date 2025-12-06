# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
#     "click",
# ]
# ///

"""Script to load a file into a pandas DataFrame and open a breakpoint.

This script takes a file path as an argument, loads it into a pandas DataFrame,
and then opens a Python debugger breakpoint for interactive exploration.

Created with assistance from aider.chat.
"""

import click
import pandas as pd


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
def main(filepath: str) -> None:
    """Load a file into a pandas DataFrame and open a breakpoint.

    Parameters
    ----------
    filepath : str
        Path to the file to load into a DataFrame.

    Notes
    -----
    The file is loaded as tab-separated values (TSV) by default, which matches
    the ICD-11 MMS format. This can be adjusted if needed for other file formats.
    """
    # Load the file into a DataFrame
    # Using tab separator to match the ICD-11 MMS SimpleTabulation format
    df = pd.read_csv(filepath, sep="\t")

    # Build a dictionary mapping chapter numbers to chapter titles
    # This allows us to look up chapter titles for blocks
    chapter_titles = {}
    for _, row in df.iterrows():
        if row["ClassKind"] == "chapter":
            chapter_titles[int(row["ChapterNo"])] = row["Title"]

    # Add ChapterTitle column for blocks
    # For each block row, look up the chapter title using its ChapterNo
    df["ChapterTitle"] = ""
    for idx, row in df.iterrows():
        if row["ClassKind"] == "block":
            chapter_no = int(row["ChapterNo"])
            df.at[idx, "ChapterTitle"] = chapter_titles.get(chapter_no, "")

    # Open breakpoint for interactive exploration of the DataFrame
    breakpoint()


if __name__ == "__main__":
    main()
