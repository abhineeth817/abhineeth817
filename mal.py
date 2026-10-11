#file to scrape myanimelist
import json
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

# Replace with your MyAnimeList username.
MAL_USERNAME = "abhineeth"
README_FILE = "README.md"

START = "<!-- ANIME-START -->"
END = "<!-- ANIME-END -->"


def fetch_json(url):
    request = Request(
        url,
        headers={"User-Agent": "GitHubAnimeProfile/1.0"}
    )

    with urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def anime_image(anime):
    images = anime.get("images", {})
    return (
        images.get("webp", {}).get("image_url")
        or images.get("jpg", {}).get("image_url")
        or ""
    )


def anime_card(anime, extra=""):
    title = anime.get("title", "Unknown title")
    url = anime.get("url", "#")
    image = anime_image(anime)

    # Escape Markdown characters in titles.
    title = title.replace("[", "\\[").replace("]", "\\]")

    card = f'<a href="{url}">'
    if image:
        card += (
            f'<img src="{image}" width="120" '
            f'alt="{title}" />'
        )
    card += f"</a><br><a href=\"{url}\"><b>{title}</b></a>"

    if extra:
        card += f"<br>{extra}"

    return f'<td align="center">{card}</td>'


def scrape_anime_list():
    base = f"https://myanimelist.net/profile/{MAL_USERNAME}"

    soup = BeautifulSoup(urlopen(base), "html.parser")
    results_top_ten = []

    for row in soup.select("#anime_favorites li.btn-fav"):
        title = row.select_one("a .title")
        link = row.select_one("a.link")
        image = row.select_one("img.image")

        results_top_ten.append({
            "title": title.get_text(strip=True) if title else "Unknown Anime",
            "url": link.get("href", "#") if link else "#",
            "image": image.get("data_src") or image.get("src", "") if image else "",
        })

    return results_top_ten

def make_section():
    # design of the section
    pass

def main():
    with open(README_FILE, "r", encoding="utf-8") as file:
        readme = file.read()

    if START not in readme or END not in readme:
        raise ValueError(
            "Add the ANIME-START and ANIME-END markers to README.md."
        )

    start_index = readme.index(START) + len(START)
    end_index = readme.index(END)

    if start_index > end_index:
        raise ValueError("Anime markers are in the wrong order.")

    print("Scraping MyAnimeList...")
    print(scrape_anime_list())

    # section = make_section()
    # updated = (
    #     readme[:start_index]
    #     + "\n\n"
    #     + section
    #     + "\n\n"
    #     + readme[end_index:]
    # )

    # with open(README_FILE, "w", encoding="utf-8") as file:
    #     file.write(updated)

    # print("Anime section updated successfully.")


if __name__ == "__main__":
    main()
