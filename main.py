# Main
import art_api as ap
import clustering

import pprint

pp = pprint.PrettyPrinter(indent=4)

def main():
    # Get a random image along with any required information about it
    img_info = ap.get_random_art()[0]
    pp.pprint(img_info)
    pp.pprint(ap.create_image_link(img_info["image_id"]))
    # Perform k-means
    # Draw palette
    # Upload to twitter


if __name__ == "__main__":
    main()

