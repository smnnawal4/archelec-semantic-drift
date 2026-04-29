"""
Télécharge les textes OCR depuis Internet Archive via ocr_url.
Lance en arrière-plan : uv run python download_ocr.py
"""
import pandas as pd
import urllib.request
import time
import os
from pathlib import Path
from tqdm import tqdm

# Config
DELAY = 0.3        # secondes entre requêtes (respecter IA)
MAX_RETRIES = 3
OUT_DIR = Path("data/raw_ocr")
OUT_DIR.mkdir(exist_ok=True)

# Charger métadonnées
meta = pd.read_csv("data/metadata/archelec.csv", low_memory=False)
leg = meta[
    (meta['contexte-election'] == 'législatives') &
    (meta['ocr_url'].notna())
].copy()

# Extraire l'année depuis la date
leg['year'] = pd.to_datetime(leg['date'], errors='coerce').dt.year

print(f"Documents à télécharger : {len(leg)}")
print(leg.groupby('year').size())

# Téléchargement
errors = []
skipped = 0
downloaded = 0

for _, row in tqdm(leg.iterrows(), total=len(leg), desc="Téléchargement"):
    year = str(int(row['year'])) if pd.notna(row['year']) else "unknown"
    doc_id = str(row['id'])
    url = str(row['ocr_url'])
    
    # Dossier de destination
    year_dir = OUT_DIR / year
    year_dir.mkdir(exist_ok=True)
    out_path = year_dir / f"{doc_id}.txt"
    
    # Skip si déjà téléchargé
    if out_path.exists() and out_path.stat().st_size > 50:
        skipped += 1
        continue
    
    # Télécharger avec retry
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as r:
                text = r.read().decode('utf-8', errors='replace')
            out_path.write_text(text, encoding='utf-8')
            downloaded += 1
            time.sleep(DELAY)
            break
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                errors.append({'id': doc_id, 'url': url, 'error': str(e)})
            time.sleep(1)

print(f"\n✅ Téléchargés : {downloaded}")
print(f"⏭️  Déjà présents (skippés) : {skipped}")
print(f"❌ Erreurs : {len(errors)}")

# Résumé par année
print("\nFichiers par année :")
for year_dir in sorted(OUT_DIR.iterdir()):
    if year_dir.is_dir():
        n = len(list(year_dir.glob("*.txt")))
        print(f"  {year_dir.name} : {n} fichiers")

# Sauvegarder les erreurs
if errors:
    pd.DataFrame(errors).to_csv("data/raw_ocr/errors.csv", index=False)
    print(f"\nErreurs sauvegardées dans data/raw_ocr/errors.csv")