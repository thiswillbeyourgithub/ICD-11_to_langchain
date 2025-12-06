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

    # Open breakpoint for interactive exploration of the DataFrame
    breakpoint()


if __name__ == "__main__":
    main()
