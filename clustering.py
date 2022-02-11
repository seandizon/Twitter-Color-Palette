# Performs k-means clustering on a provided image.

from PIL import Image, ImageDraw
from io import BytesIO
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from art_api import Art

# Get an image from a provided Art object.
def get_image(art: Art) -> np.ndarray:
    with Image.open(art.raw_image) as im:
        return np.array(im)

# Show dominant colors on a plot.
def plot_colors(clusters: np.ndarray) -> None:
    # Need to turn the cluster centers from 2d to 3d.
    # Round each value to nearest integer.
    plt.imshow(np.around(clusters.reshape((-1,1,3))).astype("uint8"))
    plt.show()

# Performs k-means clustering on an image and returns the palette.
def get_palette(art: Art, n: int) -> Image:
    # Get 3d array from image and turn into a 2d array for k-means.
    # -1 bc we don't know how many rows we'll get (technically we do, it's original row * column).
    # 3 for 3 columns: r,g,b.
    img = get_image(art).reshape((-1,3))

    # K-means clustering finds n dominant colors.
    km = KMeans(n_clusters=n).fit(img).cluster_centers_

    # Round each value to nearest integer and create color palette.
    return create_palette_image(np.around(km).astype("uint8"), "RGB")

# Get color palette of size (width, height).
def create_palette_image(c: list, color_mode: str) -> Image:
    # Dimensions for each section of colors.
    SECTION_WIDTH = 64
    SECTION_HEIGHT = 480

    # Dimension of entire picture.
    palette_width = len(c) * SECTION_WIDTH
    palette_height = SECTION_HEIGHT

    # Create blank picture.
    palette_image = Image.new(color_mode, (palette_width, palette_height))
    draw = ImageDraw.Draw(palette_image, color_mode)

    # Loop through colors and draw each color section inside of the image.
    width_offset = 0
    for color in c:
        draw.rectangle([(width_offset, 0), (width_offset+SECTION_WIDTH, SECTION_HEIGHT)], tuple(color))
        width_offset += SECTION_WIDTH

    return palette_image

# Turn Image to raw bytes.
def image_to_bytes(img: Image) -> bytes:
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()