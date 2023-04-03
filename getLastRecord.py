import os, sys
from firebase import firebase
import json

from calculate import generate_visualization


def create_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def save_string_as_JSON(json_string, path):
    json_object = json.loads(json_string)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(json_object, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    sys.tracebacklimit = 0

    ### Access Firebase realtime database
    fb_app = firebase.FirebaseApplication(
        "https://soundproxy-55bf9-default-rtdb.asia-southeast1.firebasedatabase.app/",
        None,
    )
    recent_link = fb_app.get("/Recent", None)
    loggers = fb_app.get(recent_link, None)

    store_json_path = "sample.json"
    store_vis_path = "sample.png"
    save_string_as_JSON(loggers, path=store_json_path)

    print("---------------------------")
    try:
        generate_visualization(input_path=store_json_path, output_path=store_vis_path)
    except Exception as e:
        print()
        print("---------------------------")
