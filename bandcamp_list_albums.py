#!/usr/bin/env python3

__version__ = "0.0.3"
__desc__ = "List albums from bandcamp page of artist or label."

import argparse
import json
import re
import sys
import urllib.parse

import requests
from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser(
        prog="bandcamp_list_albums",
        description=__desc__,
    )
    parser.add_argument(
        "url",
        metavar="url",
        type=str,
        help="url of desired bandcamp page",
    )
    parser.add_argument(
        "artist_name",
        metavar="artist_name",
        type=str,
        nargs="?",
        help="filter results by artist name (may be regex)",
    )
    parser.add_argument(
        "--artist-name",
        "-a",
        metavar="artist_name",
        type=str,
        help="filter results by artist name (may be regex)",
    )
    parser.add_argument(
        "--strict",
        "-s",
        action="store_true",
        help="check if artist name is equal to specified one instead of searching by regex",
    )
    parser.add_argument(
        "--print-titles",
        "--titles",
        "-t",
        action="store_true",
        help="only output album titles",
    )
    parser.add_argument(
        "--print-urls",
        "--urls",
        "-u",
        action="store_true",
        help="only output album urls",
    )
    parser.add_argument(
        "--print-json",
        "--json",
        "-j",
        action="store_true",
        help="output data as json",
    )
    args = parser.parse_args(sys.argv[1:])

    output_format_args_count = sum(
        (args.print_titles, args.print_urls, args.print_json)
    )
    if output_format_args_count > 1:
        parser.error("Too many arguments.")

    results = []
    for album in get_albums_from_page(
        args.url,
        desired_artist_name=args.artist_name,
        strict_name_comparison=args.strict,
    ):
        results.append(album)

    if args.print_json:
        print(json.dumps(results))
    else:
        if args.print_titles:
            for result in results:
                print(result["title"])
        elif args.print_urls:
            for result in results:
                print(result["url"])
        else:
            for result in results:
                print(result["title"], "--", result["url"])


def get_albums_from_page(url, desired_artist_name=None, strict_name_comparison=False):
    eprint("Downloading", url, "...")
    response = requests.get(url)
    text = response.text

    bs = BeautifulSoup(text, "html.parser")

    results = []

    default_artist_name = (
        bs.find("p", {"id": "band-name-location"}).find("span", {"class": "title"}).text
    )
    grid = bs.find("ol", {"id": "music-grid"})
    for result in grid.find_all("li", {"class": "music-grid-item"}):
        album_dict = {}
        a = result.find("a")
        album_dict["url"] = urllib.parse.urljoin(url, a["href"])
        album_title = list(a.find("p", {"class": "title"}).strings)
        album_dict["title"] = album_title[0].strip()
        if len(album_title) > 1:
            album_dict["artist_name"] = album_title[1].strip()
        else:
            album_dict["artist_name"] = default_artist_name
        # Does not work, bandcamp loads cover images dynamically
        # album_dict["cover"] = a.find("div", {"class": "art"}).find("img")["src"]

        if desired_artist_name is not None:
            if (
                not strict_name_comparison
                and re.search(
                    desired_artist_name.lower(), album_dict["artist_name"].lower()
                )
            ) or desired_artist_name.lower() == album_dict["artist_name"].lower():
                yield album_dict
        else:
            yield album_dict


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


if __name__ == "__main__":
    main()
