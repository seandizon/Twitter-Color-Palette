# This file gets/processes artwork retrieved from the Art Institute of Chicago

import requests
import pprint
from PIL import Image, ImageDraw
import numpy
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

art_url = "https://api.artic.edu/api/v1/artworks"
pp = pprint.PrettyPrinter(indent=4)

with Image.open("3.jpg") as im:
    img = numpy.array(im)

# turn 3d array to 2d array
# -1 bc we don't know how many rows we'll get (technically we do, it's original row * column)
# 3 for 3 columns: r,g,b
new_img = img.reshape((-1,3))

km = KMeans(n_clusters=10).fit(new_img)

for i in range(10):
    for j in range(3):
        # matplotlibs requires ints(1-255) or floats(0-1)
        # since centers are floats between 1-22, divide by 255 to maintain accuracy
        km.cluster_centers_[i][j] /= 255


# Need to turn the cluster centers from 2d to 3d
kc = []
for i in range(len(km.cluster_centers_)):
    kc.append([[x for x in km.cluster_centers_[i]]])

# Show palette on a graph
plt.imshow(kc)
plt.show()

# Show color
# plt.imshow([[tuple(img[540][1140])]])
# plt.show()

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