import requests
import os

# Ton DOI ou ID Zenodo
ZENODO_ID = "18487035"
README_PATH = "README.md"

# API Zenodo
url = f"https://zenodo.org/api/records/{ZENODO_ID}"
resp = requests.get(url)
resp.raise_for_status()  # Arrête si erreur API
data = resp.json()

views = data['stats']['views']
downloads = data['stats']['downloads']

# Lire le README
with open(README_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Remplacer les placeholders
new_content = content.replace("ZENODO_VIEWS", str(views))
new_content = new_content.replace("ZENODO_DOWNLOADS", str(downloads))

# Écrire le README seulement si les stats ont changé
if new_content != content:
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Zenodo stats updated: {views} vues, {downloads} téléchargements")
else:
    print("Zenodo stats unchanged. No update needed.")
