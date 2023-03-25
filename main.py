import os
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
    ### Access Firebase realtime database
    fb_app = firebase.FirebaseApplication(
        "https://soundproxy-55bf9-default-rtdb.asia-southeast1.firebasedatabase.app/",
        None,
    )
    loggers = fb_app.get("/UnityLoggers", None)

    ### Create Logger data folder
    base_path = "Unity_Loggers"
    create_folder(base_path)
    json_path = os.path.join(base_path, "json_files")
    create_folder(json_path)
    vis_path = os.path.join(base_path, "visualization")
    create_folder(vis_path)

    for scene in loggers:
        print(f"<<<<<<<<<<<<<<<<<<{scene}>>>>>>>>>>>>>>>>>>")
        scene_path = scene
        create_folder(os.path.join(json_path, scene_path))
        create_folder(os.path.join(vis_path, scene_path))
        for mode in loggers[scene]:
            print(f"==============={mode}===============")
            mode_path = scene_path + "/" + mode
            create_folder(os.path.join(json_path, mode_path))
            create_folder(os.path.join(vis_path, mode_path))
            for index in loggers[scene][mode]:
                if isinstance(loggers[scene][mode][index], str):
                    print("-------------------------")
                    store_json_path = os.path.join(
                        os.path.join(json_path, mode_path), "logger_" + index + ".json"
                    )
                    store_vis_path = os.path.join(
                        os.path.join(vis_path, mode_path), "logger_" + index + ".png"
                    )
                    # save_string_as_JSON(
                    #     loggers[scene][mode][index], path=store_json_path
                    # )
                    generate_visualization(
                        input_path=store_json_path, output_path=store_vis_path
                    )
                    print(scene + "-- || --" + mode)
                    print(index)
                    print("-------------------------")
            print("==========================================")
        print("")
