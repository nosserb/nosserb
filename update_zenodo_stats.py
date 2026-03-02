from pathlib import Path
import re

import requests


ZENODO_ID = "18487035"
README_PATH = Path(__file__).resolve().parent / "README.md"


def fetch_zenodo_stats(record_id: str) -> tuple[int, int]:
    url = f"https://zenodo.org/api/records/{record_id}"
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    data = response.json()
    stats = data.get("stats", {})
    views = stats.get("views")
    downloads = stats.get("downloads")

    if views is None or downloads is None:
        raise ValueError("Zenodo response does not contain expected 'stats.views' and 'stats.downloads'.")

    return int(views), int(downloads)


def update_readme(content: str, views: int, downloads: int) -> str:
    updated = content.replace("ZENODO_VIEWS", str(views))
    updated = updated.replace("ZENODO_DOWNLOADS", str(downloads))

    updated = re.sub(
        r"(Zenodo%20Vues-)(.*?)(-brightgreen)",
        rf"\g<1>{views}\g<3>",
        updated,
        count=1,
    )
    updated = re.sub(
        r"(Zenodo%20Téléchargements-)(.*?)(-blue)",
        rf"\g<1>{downloads}\g<3>",
        updated,
        count=1,
    )

    return updated


def main() -> None:
    views, downloads = fetch_zenodo_stats(ZENODO_ID)

    content = README_PATH.read_text(encoding="utf-8")
    updated_content = update_readme(content, views, downloads)

    if updated_content != content:
        README_PATH.write_text(updated_content, encoding="utf-8")
        print(f"Zenodo stats updated: {views} views, {downloads} downloads")
    else:
        print(f"Zenodo stats unchanged: {views} views, {downloads} downloads")


if __name__ == "__main__":
    main()
