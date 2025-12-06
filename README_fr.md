# ICD-11 vers Documents Langchain

> **Note :** Une version anglaise de ce README est disponible dans [README.md](./README.md)

Ce projet convertit les données ICD-11 (Classification internationale des maladies, 11ème révision) en objets Document langchain pour une utilisation dans des applications RAG (Retrieval-Augmented Generation) et d'autres flux de travail basés sur langchain.

Ce projet a été créé pour construire un moteur de recherche basé sur des embeddings pour les codes de classification ICD-11 via une interface web Gradio. L'interface de recherche est disponible sur [GradioSearcher](https://github.com/thiswillbeyourgithub/GradioSearcher).

Créé avec l'aide de [aider.chat](https://github.com/Aider-AI/aider/).

## Fonctionnalités

Le script `ICD11_to_langchain_documents.py` :
- Charge les données ICD-11 depuis un fichier TSV (format SimpleTabulation de l'OMS)
- Convertit chaque entrée en objet `Document` langchain
- Enrichit les blocs et catégories avec leurs titres de chapitre pour un meilleur contexte
- Sauvegarde les documents dans un fichier pickle pour un chargement facile dans d'autres scripts

Chaque Document contient :
- **page_content** : Le titre ICD-11 et le titre du chapitre pour le contexte
- **metadata** : Tous les champs disponibles des données originales (code, description, etc.)

## Utilisation

Exécutez le script avec `uv` (qui gère automatiquement les dépendances via PEP 723) :

```bash
uv run ICD11_to_langchain_documents.py chemin/vers/SimpleTabulation-ICD-11-MMS.txt
```

### Options

- `--language [fr|en]` : Langue pour les titres (par défaut : `fr` pour le français)
  - `fr` : Utilise la colonne `Title`
  - `en` : Utilise la colonne `TitleEN`
- `--remove_unused_metadata` : Supprime les champs de métadonnées avec des valeurs manquantes (par défaut : True)
- `--output CHEMIN` : Chemin de sortie pour les documents sérialisés (par défaut : `ICD-11.pickle`)

### Exemples

Convertir les données ICD-11 en français :
```bash
uv run ICD11_to_langchain_documents.py SimpleTabulation-ICD-11-MMS-fr.txt --language fr
```

Convertir les données ICD-11 en anglais avec une sortie personnalisée :
```bash
uv run ICD11_to_langchain_documents.py SimpleTabulation-ICD-11-MMS-en.txt --language en --output ICD11-en.pickle
```

## Créer le moteur de recherche

Une fois que vous avez généré le fichier pickle, vous pouvez créer une interface de recherche avec GradioSearcher :

```bash
# Installer GradioSearcher
uv pip install gradioSearch -U

# Créer le moteur de recherche
python -m gradioSearch --db_path ./ICD-11-v0.2.0.pickle --embedding_model "minishlab/potion-multilingual-128M" --output-db-path ./faiss-ICD-11_v2 --metadata_keys="Code,BrowserLink,Foundation URI, Linearization URI"
```

Cela créera une interface de recherche basée sur des embeddings qui permet de rechercher efficacement dans les codes de classification ICD-11.

## Obtenir les données ICD-11

### Version française

1. Allez sur https://icd.who.int/browse/2025-01/mms/fr
2. Cliquez sur `Info` puis sur `Fichier du tableur`
3. Téléchargez le fichier `.txt`
4. Vérifiez le hash SHA-256 :

```
d640109d998f8b2cb7a22a31574a10ec7a03b67a47f786e9ca7f3d72cbabef25  SimpleTabulation-ICD-11-MMS-fr.txt
4c7dd18cf6204c9df84b8624cfc123bed9838dc9be858e82f20ecd754e3f371a  SimpleTabulation-ICD-11-MMS-fr.xlsx
c14f94ad6fe0e75c1993ea38c29a5886bab0849dd507cd5f4ae710a11793e2e1  SimpleTabulation-ICD-11-MMS-fr.zip
```

### Version anglaise

1. Allez sur https://icd.who.int/browse/2025-01/mms/en
2. Cliquez sur `Info` puis sur `Spreadsheet file` (Fichier du tableur)
3. Téléchargez le fichier `.txt`

## Prérequis

Le script utilise les dépendances inline PEP 723 (Python 3.11+) :
- pandas
- click
- langchain_core

Aucune installation séparée n'est nécessaire lors de l'utilisation de `uv run`.
