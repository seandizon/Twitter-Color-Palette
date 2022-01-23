# This file gets/processes artwork retrieved from the Art Institute of Chicago

import requests
import time

class Art:
    def __init__(self):
        img = self._get_random_art_()
        self.info = img
        self.artist = img["artist_title"] if img["artist_title"] else "Unknown"
        self.title = img["title"] if img["title"] else "Unknown"
        self.date = img["date_display"] if img["date_display"] else "Unknown"
        self.link = "https://www.artic.edu/artworks/" + str(img["id"])

        # Download image
        self.image_link = self._create_image_link_(img["image_id"])
        self._raw_image = requests.get(self.image_link, stream=True).raw

    @property
    def caption(self):
        return f"{self.artist}\n{self.title}\n{self.date}\n{self.link}"

    @property
    def raw_image(self):
        return self._raw_image

    def _get_random_art_(self) -> list:
        art_url = "https://api.artic.edu/api/v1/artworks/search"
        payload = self._get_payload_()
        AIC_header = {"AIC-User-Agent": "Twitter Color Palette Bot (email soon)"}
        r = requests.post(art_url, json=payload, headers=AIC_header)
        print(r.json()["pagination"]) # see number of results
        return r.json()["data"][0]

    def _create_image_link_(self, image_id: str) -> str:
        return f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg"

    def _get_payload_(self) -> dict:
        return {
            "limit": 1,
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
                                        "bowl", "weapon"
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
                                            "watercolor", "american arts"
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