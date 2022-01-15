# This file gets/processes artwork retrieved from the Art Institute of Chicago

import requests
import pprint
from PIL import Image, ImageDraw
import numpy
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

art_url = "https://api.artic.edu/api/v1/artworks"
pp = pprint.PrettyPrinter(indent=4)

# This function will eventually change to get an image using the AIC api.
# Current version is for testing purposes.
def get_image(img_name: str) -> numpy.ndarray:
    with Image.open(img_name) as im:
        return numpy.array(im)

# Matplotlibs requires ints (1-255) or floats (0.00-1.00).
# Since centers are floats between 1-255, divide by 255 to maintain accuracy.
def convert_to_float_points(clusters: numpy.ndarray, n: int) -> None:
    for i in range(n):
        for j in range(3):
            clusters[i][j] /= 255

# Show dominant colors on a plot.
def plot_colors(clusters: numpy.ndarray, n: int) -> None:
    # Need to turn the cluster centers from 2d to 3d.
    kc = []
    for i in range(n):
        kc.append([[x for x in clusters[i]]])

    # Show palette on a graph.
    plt.imshow(kc)
    plt.show()

# Will eventually return an image.
def get_palette(n: int) -> None:
    # Get 3d array from image and turn into a 2d array for k-means.
    # -1 bc we don't know how many rows we'll get (technically we do, it's original row * column).
    # 3 for 3 columns: r,g,b.
    img = get_image("5.jpg").reshape((-1,3))

    # K-means clustering finds n dominant colors.
    km = KMeans(n_clusters=n).fit(img).cluster_centers_

    # Convert centers to points for plotting.
    convert_to_float_points(km, n)

    # Plot.
    plot_colors(km, n)

get_palette(10)

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