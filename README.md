# Arkindex × Archelec

Analyse textuelle (NLP) du corpus **Archelec** (professions de foi électorales) à partir des transcriptions produites dans **Arkindex**. Le dépôt regroupe le prétraitement, des modèles de plongements lexicaux (Word2Vec), une étude de **dérive sémantique** dans le temps, et un **modèle de sujets** (LDA) croisé avec les familles politiques, professions et tranches d’âge.

## Prérequis

- **Python 3.13** (voir `.python-version`)
- Gestion des dépendances : **uv** (recommandé, `uv.lock` présent) ou `pip`

## Installation

```bash
cd arkindex_archelec
uv sync
```

Sans **uv** : créer un environnement virtuel puis installer les paquets listés dans `dependencies` de `pyproject.toml` (par ex. `pip install gensim matplotlib numpy pandas scikit-learn scipy seaborn spacy tqdm` en adaptant les versions si besoin).

Modèle spaCy utilisé dans le notebook de prétraitement :

```bash
python -m spacy download fr_core_news_lg
```

## Structure du dépôt

| Élément | Rôle |
|--------|------|
| `data/metadata/` | Fichiers tabulaires (`corpus_complet.csv`, `archelec.csv`, …) |
| `data/raw_ocr/`, `data/raw/`, `data/processed/` | Textes OCR et jeux dérivés pour les notebooks |
| `notebooks/` | Chaîne d’analyse numérotée `01` → `06` |
| `src/extract_text.py` | Extraction des transcriptions depuis une base SQLite exportée par Arkindex |
| `src/ocr.py` | Utilitaires OCR |
| `results/` | Sorties tabulaires (scores de drift, tables topic modeling, …) |
| `report/` | Rapport (`NLP_report.pdf`) et figures exportées |

## Notebooks (ordre conseillé)

1. **01 — Exploration** — Corpus texte (plusieurs années) et métadonnées Archelec  
2. **02 — Preprocessing** — Normalisation, lemmatisation (spaCy), construction des corpus tokenisés  
3. **03 — Word2Vec** — Entraînement par fenêtre temporelle  
4. **04 — Détection du drift sémantique** — Comparaison d’espaces vectoriels entre périodes  
5. **05 — Études de cas qualitatives** — Lectures ciblées et visualisations  
6. **06 — Topic modeling × familles politiques** — LDA (Gensim), profils thématiques et lift par groupe  

Les chemins dans les notebooks supposent d’être exécutés depuis le dossier `notebooks/` (références du type `../data/...`).

## Dépendances principales

Gensim, spaCy, scikit-learn, pandas, NumPy, SciPy, matplotlib, seaborn, tqdm — voir `pyproject.toml` pour les versions figées.

