import requests

# Ton ID Zenodo
zenodo_id = "18487035"
url = f"https://zenodo.org/api/records/{zenodo_id}"

resp = requests.get(url)
data = resp.json()

views = data['stats']['views']
downloads = data['stats']['downloads']

# Lire le README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Remplacer les placeholders
content = content.replace("ZENODO_VIEWS", str(views))
content = content.replace("ZENODO_DOWNLOADS", str(downloads))

# Écrire le README mis à jour
with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print(f"Zenodo stats updated: {views} views, {downloads} downloads")
