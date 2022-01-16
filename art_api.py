# This file gets/processes artwork retrieved from the Art Institute of Chicago

import requests
import pprint

art_url = "https://api.artic.edu/api/v1/artworks"
pp = pprint.PrettyPrinter(indent=4)

# Example way for api get requests
# payload = {
#     "limit": 2,
#     "fields": ','.join([
#         "id",
#         "title",
#         "artist_display",
#         "image_id",
#         "date_display",
#         "medium_display"
#     ])
# }
#
# r = requests.get(art_url, params=payload)
# print(r.url)
# pp.pprint(r.json()["data"])