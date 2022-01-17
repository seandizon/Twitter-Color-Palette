# This file gets/processes artwork retrieved from the Art Institute of Chicago

import requests
import time

def get_random_art() -> list:
    art_url = "https://api.artic.edu/api/v1/artworks/search"
    payload = get_payload()

    r = requests.post(art_url, json=payload)

    return r.json()["data"]

def create_image_link(image_id: str) -> str:
    return f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg"

def get_payload() -> dict:
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
            "is_public_domain"
        ]),
        "boost": False,
        "query": {
            "function_score": {
                "query": {
                    "bool": {
                        "filter": [
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