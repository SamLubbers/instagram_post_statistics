# Instagram post statistics

This project was created to facilitate the content analysis of different
instagram pages by automating the long manual process of downloading post data
from Instagram. 

## Prerequisites

- Python >= 3.8 
- Install Python requirements by running in your terminal: `pip install -r
  requirements.txt`

## Run

It works as follows:

1. Download instagram statistics in JSON format. You can do this by going to the
   Instagram page you wish to analyse and append `?__a=1` to the URL. For
   example: `https://www.instagram.com/politiek_bij1/?__a=1`. Once the JSON data
   loads you can download it to a file called `instagram_page_statistics.json`
  1. Note: when you navigate to that page you can only get the first 25 posts.
     To get more posts check out [this article](https://dev.to/iankerins/the-easy-way-to-build-an-instagram-spider-using-python-scrapy-graphql-4gko)
2. In your terminal run `python instagram_data_extractor.py`. This script will
   do the following for each of the posts that contain pictures (not videos):
  1. download the image and store it in a jpg file. If a post contains multiple
     images it will download all of them
  2. download the caption and store it in a txt file
  3. store the number of likes, number of comments and other relevant metadata
     of the post into a csv file.

You can now load the images and text files into a content analysis software like
[Atlas.ti](https://atlasti.com/) to do content analysis.

Subsequently, you can export your content analysis code, and together with the
post statistics you can do statistical analysis in a program like
[SPSS](https://www.ibm.com/products/spss-statistics)

## Configuration

Change the START_DATE and END_DATE in the python script
`instagram_data_extractor.py` to specifiy the posts that are relevant for your
analysis. The script will only keep those posts, and discard all others

## Questions

If something doesn't work as expect or you have any questions open an issue in
this repository and @mention me. 

