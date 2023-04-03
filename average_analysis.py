import argparse
import os
import copy
from generate_analysis import generate_result

ANALYSIS_DICT = {
    "RW_FOCUS": [],
    "VR_FOCUS": [],
    "RW_PERIPHERAL": [],
    "VR_PERIPHERAL": [],
}


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", default="/blind_people_data")
    parser.add_argument("-o", "--output", default="result.txt")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_parser()

    result_analysis = {}
    total_user_count = 0
    fp = open(args.output, "w")

    if os.path.isdir(args.input_dir):
        for user in os.listdir(args.input_dir):
            user_path = os.path.join(os.path.join(args.input_dir, user), "json_files")
            if not os.path.isdir(user_path):
                continue
            total_user_count += 1
            for scene in os.listdir(user_path):
                scene_path = os.path.join(user_path, scene)
                if not os.path.isdir(scene_path):
                    continue
                # fp.write(f"<<<<<<<<<<<<<<<<<<{scene}>>>>>>>>>>>>>>>>>>\n")
                for mode in os.listdir(scene_path):
                    mode_path = os.path.join(scene_path, mode)
                    if not os.path.isdir(mode_path):
                        continue
                    # fp.write(f"==============={mode}===============\n\n")
                    print("=====================")
                    key = scene + "_" + mode
                    if key not in result_analysis:
                        result_analysis[key] = [0, 0, 0, 0, 0]
                    total_count = 0
                    temp = [0, 0, 0, 0, 0]
                    for logger in os.listdir(mode_path):
                        if not logger.endswith(".json"):
                            continue
                        result = generate_result(os.path.join(mode_path, logger))

                        for i in range(len(result)):
                            temp[i] += result[i]
                        total_count += 1

                    for i in range(len(temp)):
                        temp[i] = temp[i] / total_count

                    for i in range(len(temp)):
                        result_analysis[key][i] += temp[i]
    print(total_user_count)
    for type in result_analysis:
        fp.write(f"---------------{type}---------------\n")
        fp.write(f"Hit Accuracy: {result_analysis[type][0]/total_user_count}\n")
        fp.write(f"Hit Error Rate: {result_analysis[type][1]/total_user_count}\n")
        fp.write(f"Number of Miss Event: {result_analysis[type][2]/total_user_count}\n")
        fp.write(f"Number of Miss Touch: {result_analysis[type][3]/total_user_count}\n")
        fp.write(
            f"Overall average delay is:{result_analysis[type][4]/total_user_count}\n"
        )
        fp.write(f"-------------------------------------\n\n")
        # fp.write(f"==================================\n\n")
    fp.close()
