# Main

import art_api as ap
import clustering as cl
import twitter_api as tw

import pprint

pp = pprint.PrettyPrinter(indent=4)

def main():
    # Get a random image along with any required information about it.
    artwork = ap.Art()
    pp.pprint(artwork.info)
    print(artwork.caption)

    # Perform k-means and draw.
    NUM_CLUSTERS = 10
    palette = cl.get_palette(artwork, NUM_CLUSTERS)
    palette.show()

    # Upload to twitter.
    # api = tw.get_api()
    # api.update_status(status=artwork.caption)



if __name__ == "__main__":
    main()

