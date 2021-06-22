import json
import shutil
import requests
import pandas as pd
import datetime as dt
from functools import partial

START_DATE = "2020_09_17"
END_DATE = "2021_03_18"
DATE_FORMAT = "%Y_%m_%d"


def load_posts():
    with open('instagram_page_statistics.json') as f:
        posts = json.load(f)

    return posts


def is_in_date_range(post, start_date, end_date):
    start_datetime = dt.datetime.strptime(start_date, DATE_FORMAT)
    end_datetime = dt.datetime.strptime(end_date, DATE_FORMAT)
    datetime = dt.datetime.fromtimestamp(post['taken_at_timestamp'])
    return start_datetime < datetime and datetime < end_datetime


def is_gallery(post):
    return post["__typename"] == "GraphSidecar"


def get_gallery_items(post):
    items = post['edge_sidecar_to_children']["edges"]
    items = [item["node"] for item in items]
    return items


def contains_image(post):
    """return True if the post is an image, or is a gallery that contains at least one image"""
    if post['is_video']:
        return False
    if is_gallery(post):
        items = get_gallery_items(post)
        all_videos = all([item['is_video'] for item in items])
        if all_videos:
            return False

    return True


def filter_posts(posts):
    posts = [post['node'] for post in posts]  # easier access
    posts = list(filter(partial(is_in_date_range, start_date=START_DATE, end_date=END_DATE), posts))
    print(f"{len(posts)} posts between the dates {START_DATE} and {END_DATE}")
    posts = list(filter(contains_image, posts))
    print(f"{len(posts)} of those posts is an image, or is a gallery with images")
    return posts


def extract_media_url(media):
    """extracts the url of a media item: an image post, or an image within a gallary

    I extract the data from the first items in "display_resources" instead of the standard "display_url" because this is
    the lowest resolution available
    """
    return media["display_resources"][0]["src"]


def get_post_urls(post):
    if is_gallery(post):
        items = get_gallery_items(post)
        # filter out videos from the gallery
        image_items = [item for item in items if not item['is_video']]
        n_videos = len(items) - len(image_items)
        if n_videos > 0:
            print(f"WARNING: {n_videos} video(s) omitted from gallery of post with id: {post['id']}")
        urls = [extract_media_url(item) for item in image_items]
    else:
        urls = [extract_media_url(post)]

    return urls


def download_image(url, image_title, i):
    """downloads image and returns the file name"""
    file_name = f'{image_title}_{i+1}.jpg'
    response = requests.get(url, stream=True)
    with open(f'data/{file_name}', 'wb') as f:
        shutil.copyfileobj(response.raw, f)
    del response
    return file_name


def extract_data(post):
    return {
        "date": dt.datetime.fromtimestamp(post["taken_at_timestamp"]).strftime(DATE_FORMAT),
        "account": post["owner"]["username"],
        "number_of_likes": post["edge_media_preview_like"]["count"],
        "number_of_comments": post["edge_media_to_comment"]["count"],
        "urls": get_post_urls(post),
        "caption": post["edge_media_to_caption"]["edges"][0]["node"]["text"],
        "id": post["id"]
    }


def extract_images(data):
    file_names = []
    for i, url in enumerate(data["urls"]):
        file_name = download_image(url, data["file_name"], i)
        file_names.append(file_name)
    del data['urls']
    data["file_name(s)"] = file_names
    del data["file_name"]


def store_caption(data):
    file_name = f"{data["account"]}_{data['date']}_{data['id']}"
    with open(f"data/{file_name}.txt", 'w') as f:
        f.write(data["caption"])

    data["file_name"] = file_name  # store in data to reuse the same name for images


def main():
    posts = load_posts()
    posts = filter_posts(posts)
    data_json = map(extract_data, posts)
    for entry in data_json:
        store_caption(entry)
        extract_images(entry)
    df = pd.DataFrame(data_json)
    df.to_csv("instagram_page_statistics.csv", index=False)


if __name__ == "__main__":
    main()
