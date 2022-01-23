# Main

import art_api as ap
import clustering as cl
import twitter_api as tw

import pprint

pp = pprint.PrettyPrinter(indent=4)

def main():
    # Get a random image along with any required information about it.
    # img_info = ap.get_random_art()[0]
    # pp.pprint(img_info)
    #
    # # Perform k-means and draw.
    # NUM_CLUSTERS = 10
    # img_url = ap.create_image_link(img_info["image_id"])
    # print(img_url)
    # cl.get_palette(img_url, NUM_CLUSTERS)

    # Upload to twitter.
    api = tw.get_api()
    api.update_status(status="Test with 1.1")



if __name__ == "__main__":
    main()

