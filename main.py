# Main
import art_api as ap
import clustering as cl

import pprint

pp = pprint.PrettyPrinter(indent=4)

def main():
    # Get a random image along with any required information about it
    img_info = ap.get_random_art()[0]
    pp.pprint(img_info)

    # Perform k-means
    NUM_CLUSTERS = 10
    img_url = ap.create_image_link(img_info["image_id"])
    print(img_url)
    cl.get_palette(img_url, NUM_CLUSTERS)

    # Draw palette
    # Upload to twitter

if __name__ == "__main__":
    main()

