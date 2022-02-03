# Color Palette Twitter Bot
A bot that gets random artwork from the Art Institute of Chicago (AIC), generates a color palette based on the artwork, and uploads both images to Twitter.

#### Artwork and generated palette
<span>
  <img title="Artwork retrieved from AIC" src="https://user-images.githubusercontent.com/43098042/152429502-dc1e95b0-1314-43b5-a8b8-9516d980ec27.png" height="350">
  <img title="Generated palette" src="https://user-images.githubusercontent.com/43098042/152431138-673032ce-349e-4d72-9131-9935590134ed.png" height="350">
 </span>

#### Final tweet
<img title="Created tweet" src="https://user-images.githubusercontent.com/43098042/152433291-dce232e8-b1b2-40e3-ab88-db4234486311.png" height="400">

## Installation and running

1. Install [python](https://www.python.org/).

2. Clone this repo.

3. Install the requirements.
```
pip install -r requirements.txt
```

4. Create a [Twitter application](https://developer.twitter.com/en). (Requires a developer account with [Elevated](https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api) access)

5. Create a `.env` file in the same folder as the repo for the environmental variables (with no quotes around any value). It will contain:
   - Your email to identify who is accessing the AIC API
   - Keys associated with your Twitter application to access the Twitter API

```
CONSUMER_KEY=
CONSUMER_SECRET=
ACCESS_TOKEN=
ACCESS_SECRET=
EMAIL=
```


6. Run main
```
python main.py
```
