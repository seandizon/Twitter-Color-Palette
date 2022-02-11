# This file gets/processes artwork retrieved from the Art Institute of Chicago

import requests
import time
import os
import pprint

class Art:
    def __init__(self):
        img = self._get_random_art_()
        self.artist = img["artist_title"] if img["artist_title"] else "Artist unknown"
        self.date = img["date_display"] if img["date_display"] else "Date unknown"
        self.link = "https://www.artic.edu/artworks/" + str(img["id"])

        # Make sure the title fits in the tweet.
        if img["title"]:
            max_tweet_len = 280
            current_tweet_len = len(self.artist) + len(self.date) + len(self.link) + 3 # 3 newlines

            if (len(img["title"]) + current_tweet_len) <= max_tweet_len:
                self.title = img["title"]
            else:
                available_characters = max_tweet_len - current_tweet_len - 3 # ellipsis
                self.title = img["title"][:available_characters] + "..."
        else:
            self.title = "Title unknown"

        # For downloading the image.
        self.image_link = f"https://www.artic.edu/iiif/2/{img['image_id']}/full/843,/0/default.jpg"

    @property
    def caption(self) -> str:
        return f"{self.artist}\n{self.title}\n{self.date}\n{self.link}"

    @property
    def raw_image(self) -> bytes:
        attempts = 0
        done = False
        while not done:
            try:
                r = requests.get(self.image_link, stream=True)
                r.raise_for_status()
                done = True
            except requests.exceptions.RequestException:
                attempts += 1
                if attempts >= 3:
                    raise

        return r.raw

    def _get_random_art_(self) -> list:
        art_url = "https://api.artic.edu/api/v1/artworks/search"
        payload = self._get_payload_()
        AIC_header = {"AIC-User-Agent": f'Twitter Color Palette Bot ({os.environ.get("EMAIL")})'}

        attempts = 0
        done = False
        while not done:
            try:
                r = requests.post(art_url, json=payload, headers=AIC_header)
                r.raise_for_status()
                done = True
            except requests.exceptions.RequestException:
                attempts += 1
                if attempts >= 3:
                    raise

        # Just to see retrieved data.
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(r.json()["data"])

        return r.json()["data"][time.time_ns() % 3]

    def _get_payload_(self) -> dict:
        return {
            "limit": 3,
            "fields": ','.join([
                # Included in the caption for the tweet.
                "artist_title",
                "title",
                "date_display",
                "id", # For link to artwork on AIC website.

                # For link to download image for processing.
                "image_id",

                # Mostly just to see artwork details to further help refine the query.
                "is_public_domain",     # Just to see that it's in the public domain.
                "colorfulness",         # See how colorfulness is applied to artwork.
                "classification_titles" # If there is artwork I don't want to be included in the query,
                                        # I can find the classification title and put it in the must_not
                                        # query section.
            ]),
            "boost": False,
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "must_not": {
                                "terms": {
                                    # Artwork I want to ignore.
                                    "classification_titles.keyword": [
                                        "sculpture", "metal", "graphite", "glass",
                                        "furniture", "stoneware", "ceramics", "jade",
                                        "brass", "metalwork", "silver", "jewelry",
                                        "bowl", "weapon", "pen and ink drawings"
                                    ]
                                }
                            },
                            "filter": [
                                {
                                    "range": {
                                        # Don't want artwork only having the colors black and white.
                                        "colorfulness": {
                                            "gte": 1
                                        }
                                    }
                                },
                                {
                                    "terms": {
                                        # Artwork I want.
                                        "classification_titles.keyword": [
                                            "painting", "asian art", "modern and contemporary art",
                                            "watercolor", "american arts", "drawings (visual works)"
                                        ]
                                    }
                                },
                                {
                                    "term": {
                                        # Make sure artwork is copyright free.
                                        "is_public_domain": True
                                    }
                                },
                                {
                                    "exists": {
                                        # Make sure artwork can be downloaded.
                                        "field": "image_id"
                                    }
                                }
                            ]
                        }
                    },
                    "boost_mode": "replace",
                    "random_score": {
                        # Retrieves random artwork.
                        "seed": time.time_ns(),
                        "field": "id"
                    }
                }
            }
        }