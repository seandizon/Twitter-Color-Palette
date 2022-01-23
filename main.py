# Main

import art_api as ap
import clustering as cl
import twitter_api as tw

def main():
    # Get a random image along with any required information about it.
    artwork = ap.Art()

    # Perform k-means and draw palette.
    palette = cl.get_palette(artwork, 10)

    # Upload to twitter.
    api = tw.get_api()

    pictures = [
        api.simple_upload(filename="art", file=artwork.raw_image).media_id,
        api.simple_upload(filename="palette", file=cl.image_to_bytes(palette)).media_id
    ]

    api.update_status(status=artwork.caption, media_ids=pictures)

if __name__ == "__main__":
    main()

