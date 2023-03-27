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

    fp = open("Unity_Loggers/result.txt", "w")

    for scene in loggers:
        print(f"<<<<<<<<<<<<<<<<<<{scene}>>>>>>>>>>>>>>>>>>")
        fp.write(f"<<<<<<<<<<<<<<<<<<{scene}>>>>>>>>>>>>>>>>>>\n")
        scene_path = scene
        create_folder(os.path.join(json_path, scene_path))
        create_folder(os.path.join(vis_path, scene_path))
        for mode in loggers[scene]:
            print(f"==============={mode}===============")
            fp.write(f"==============={mode}===============\n")
            mode_path = scene_path + "/" + mode
            create_folder(os.path.join(json_path, mode_path))
            create_folder(os.path.join(vis_path, mode_path))

            analysis = [0, 0, 0, 0, 0, 0, 0]
            total_count = 0
            for index in loggers[scene][mode]:
                if isinstance(loggers[scene][mode][index], str):
                    print("-------------------------")
                    store_json_path = os.path.join(
                        os.path.join(json_path, mode_path), "logger_" + index + ".json"
                    )
                    store_vis_path = os.path.join(
                        os.path.join(vis_path, mode_path), "logger_" + index + ".png"
                    )
                    save_string_as_JSON(
                        loggers[scene][mode][index], path=store_json_path
                    )
                    result = generate_visualization(
                        input_path=store_json_path, output_path=store_vis_path
                    )

                    temp = []
                    for i in range(len(analysis)):
                        temp.append(analysis[i] + result[i])
                    analysis = temp
                    total_count += 1

                    # print(scene + "-- || --" + mode)
                    # print(index)
                    print("-------------------------")
            for i in range(len(analysis)):
                analysis[i] = analysis[i] / total_count

            fp.write(f"Overall average delay is:{analysis[0]}\n")
            fp.write(f"Number of Miss Event: {analysis[1]}\n")
            fp.write(f"Number of Miss Touch: {analysis[2]}\n")
            fp.write(f"Number of Hit Correct Event: {analysis[3]}\n")
            fp.write(f"Number of Hit Error Event: {analysis[4]}\n")
            fp.write(f"Total number of event is: {analysis[5]}\n")
            fp.write(f"Hit Accuracy: {analysis[6]}\n")
            fp.write(f"==================================\n\n")

            print("==========================================")
        print("")
