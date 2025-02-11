import os
import pathlib
from time import sleep

import requests


def get_cats():
    print("Добываются коты")
    media_dir = pathlib.Path(__file__).parent / "media"
    media_dir.mkdir(exist_ok=True)
    media_dir_content = os.listdir(media_dir)
    if len(media_dir_content) >= 45:
        print("Коты уже есть")
        return
    for i in range(1, 46):
        print("Кот", i)
        while True:
            try:
                resp = requests.get("https://cataas.com/cat")
                break
            except:
                sleep(1)
        with open(f"media/{i}.jpg", "wb") as file:
            file.write(resp.content)