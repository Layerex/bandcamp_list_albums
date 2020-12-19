# bandcamp_name_your_price_dl

List albums from bandcamp page of artist or label.

## Installation

```sh
pip install bandcamp-list-albums
```

## Usage

```text
usage: bandcamp_list_albums [-h] [--artist-name artist_name] [--strict] [--print-titles] [--print-urls] [--json] url [artist_name]

List albums from bandcamp page of artist or label.

positional arguments:
  url                   url of desired bandcamp page
  artist_name           filter results by artist name (may be regex)

optional arguments:
  -h, --help            show this help message and exit
  --artist-name artist_name, -a artist_name
                        filter results by artist name (may be regex)
  --strict, -s          check if artist name is equal to specified one instead of searching by regex
  --print-titles, -t    only output album titles
  --print-urls, -u      only output album urls
  --json                output data as json
```
