from os.path import dirname, join

from pysitemap import crawler

export_dir = dirname(__file__)

export_path = join(export_dir, "bot_data", "html")

exclude = [
    "https://bot.pokestarfan.ga/&",
    ".txt",
    ".css",
    ".js",
    "https://bot.pokestarfan.ga/public",
    "https://bot.pokestarfan.ga/error",
    "?syntax=1",
    ".webmanifest",
    ".woff2",
    ".png",
    ".jpg",
    ".jpeg",
    ".svg",
    ".ico",
    "https://bot.pokestarfan.ga/cdn-cgi",
]

crawler(
    "https://bot.pokestarfan.ga",
    out_file=join(export_path, "sitemap.xml"),
    exclude_urls=exclude,
)
crawler(
    "https://bot.pokestarfan.ga",
    out_file=join(export_path, "sitemap.txt"),
    out_format="txt",
    exclude_urls=exclude,
)
