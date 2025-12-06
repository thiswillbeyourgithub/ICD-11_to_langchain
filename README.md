# ICD-11 to Langchain Documents

> **Note:** A French version of this README is available at [README_fr.md](./README_fr.md)

This project converts ICD-11 (International Classification of Diseases, 11th Revision) data into langchain Document objects for use in RAG (Retrieval-Augmented Generation) applications and other langchain-based workflows.

Created with assistance from [aider.chat](https://github.com/Aider-AI/aider/).

## What It Does

The `ICD11_to_langchain_documents.py` script:
- Loads ICD-11 data from a TSV file (WHO's SimpleTabulation format)
- Converts each entry into a langchain `Document` object
- Enriches blocks and categories with their chapter titles for better context
- Saves the documents as a pickle file for easy loading in other scripts

Each Document contains:
- **page_content**: The ICD-11 title and chapter title for context
- **metadata**: All available fields from the original data (code, description, etc.)

## Usage

Run the script using `uv` (which handles dependencies automatically via PEP 723):

```bash
uv run ICD11_to_langchain_documents.py path/to/SimpleTabulation-ICD-11-MMS.txt
```

### Options

- `--language [fr|en]`: Language for titles (default: `fr` for French)
  - `fr`: Uses the `Title` column
  - `en`: Uses the `TitleEN` column
- `--remove_unused_metadata`: Remove metadata fields with missing values (default: True)
- `--output PATH`: Output path for pickled documents (default: `ICD-11.pickle`)

### Examples

Convert French ICD-11 data:
```bash
uv run ICD11_to_langchain_documents.py SimpleTabulation-ICD-11-MMS-fr.txt --language fr
```

Convert English ICD-11 data with custom output:
```bash
uv run ICD11_to_langchain_documents.py SimpleTabulation-ICD-11-MMS-en.txt --language en --output ICD11-en.pickle
```

## Getting ICD-11 Data

### French Version

1. Go to https://icd.who.int/browse/2025-01/mms/fr
2. Click on `Info` then on `Fichier du tableur` (Spreadsheet file)
3. Download the `.txt` file
4. Verify the SHA-256 hash:

```
d640109d998f8b2cb7a22a31574a10ec7a03b67a47f786e9ca7f3d72cbabef25  SimpleTabulation-ICD-11-MMS-fr.txt
4c7dd18cf6204c9df84b8624cfc123bed9838dc9be858e82f20ecd754e3f371a  SimpleTabulation-ICD-11-MMS-fr.xlsx
c14f94ad6fe0e75c1993ea38c29a5886bab0849dd507cd5f4ae710a11793e2e1  SimpleTabulation-ICD-11-MMS-fr.zip
```

### English Version

1. Go to https://icd.who.int/browse/2025-01/mms/en
2. Click on `Info` then on `Spreadsheet file`
3. Download the `.txt` file

## Requirements

The script uses PEP 723 inline dependencies (Python 3.11+):
- pandas
- click
- langchain_core

No separate installation needed when using `uv run`.
