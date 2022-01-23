# This file gets/processes artwork retrieved from the Art Institute of Chicago

import requests
import time
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)

from dotenv import load_dotenv
load_dotenv()

class Art:
    def __init__(self):
        img = self._get_random_art_()
        self.info = img
        self.artist = img["artist_title"] if img["artist_title"] else "Unknown"
        self.date = img["date_display"] if img["date_display"] else "Unknown"
        self.link = "https://www.artic.edu/artworks/" + str(img["id"])

        if img["title"]:
            max_tweet_len = 280
            current_tweet_len = len(self.artist) + len(self.date) + len(self.link) + 3 # 3 newlines

            if (len(img["title"]) + current_tweet_len) <= max_tweet_len:
                self.title = img["title"]
            else:
                available_characters = max_tweet_len - current_tweet_len - 3 # ellipsis
                self.title = img["title"][:available_characters] + "..."

        # Download image
        self.image_link = self._create_image_link_(img["image_id"])

    @property
    def caption(self):
        return f"{self.artist}\n{self.title}\n{self.date}\n{self.link}"

    @property
    def raw_image(self):
        return requests.get(self.image_link, stream=True).raw

    def _get_random_art_(self) -> list:
        art_url = "https://api.artic.edu/api/v1/artworks/search"
        payload = self._get_payload_()
        AIC_header = {"AIC-User-Agent": f'Twitter Color Palette Bot ({os.environ.get("EMAIL")})'}
        r = requests.post(art_url, json=payload, headers=AIC_header)
        print(r.request.headers)
        print(r.json()["pagination"]) # see number of results
        pp.pprint(r.json()["data"])
        return r.json()["data"][time.time_ns() % 3]

    def _create_image_link_(self, image_id: str) -> str:
        return f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg"

    def _get_payload_(self) -> dict:
        return {
            "limit": 3,
            "fields": ','.join([
                # to be included in the artwork caption
                "artist_title",
                "title",
                "date_display",
                "id", # for link

                # needed to download image for processing
                "image_id",

                # make sure it's copyright free
                "is_public_domain",
                "colorfulness",
                "classification_titles"
            ]),
            "boost": False,
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "must_not": {
                                "terms": {
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
                                        "colorfulness": {
                                            # black and white artwork have a value of 0,
                                            # we want to avoid those
                                            "gte": 1
                                        }
                                    }
                                },
                                {
                                    "terms": {
                                        "classification_titles.keyword": [
                                            "painting", "asian art", "modern and contemporary art",
                                            "watercolor", "american arts", "drawings (visual works)"
                                        ]
                                    }
                                },
                                {
                                    "term": {
                                        "is_public_domain": True # copyright free
                                    }
                                },
                                {
                                    "exists": {
                                        "field": "image_id" # downloadable
                                    }
                                }
                            ]
                        }
                    },
                    "boost_mode": "replace",
                    "random_score": {
                        "seed": time.time_ns(),
                        "field": "id"
                    }
                }
            }
        }