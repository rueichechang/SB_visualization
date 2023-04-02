import argparse
import os
import copy
from generate_analysis import generate_type_analysis

ANALYSIS_DICT = {
    "RW_FOCUS": [0, 0, 0, 0, 0],
    "VR_FOCUS": [0, 0, 0, 0, 0],
    "RW_PERIPHERAL": [0, 0, 0, 0, 0],
    "VR_PERIPHERAL": [0, 0, 0, 0, 0],
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
                        result_analysis[key] = copy.deepcopy(ANALYSIS_DICT)
                    total_count = 0
                    temp = copy.deepcopy(ANALYSIS_DICT)
                    for logger in os.listdir(mode_path):
                        if not logger.endswith(".json"):
                            continue
                        result = generate_type_analysis(os.path.join(mode_path, logger))

                        for type in temp:
                            for i in range(len(temp[type])):
                                temp[type][i] += result[type][i]
                        total_count += 1

                    for type in temp:
                        for i in range(len(temp[type])):
                            temp[type][i] = temp[type][i] / total_count

                    for type in result_analysis[key]:
                        for i in range(len(result_analysis[key][type])):
                            result_analysis[key][type][i] += temp[type][i]

    print(total_user_count)
    for key in result_analysis:
        fp.write(f"==============={key}===============\n")
        for type in result_analysis[key]:
            fp.write(f"---------------{type}---------------\n")
            fp.write(
                f"Hit Accuracy: {result_analysis[key][type][0]/total_user_count}\n"
            )
            fp.write(
                f"Hit Error Rate: {result_analysis[key][type][1]/total_user_count}\n"
            )
            fp.write(
                f"Number of Miss Event: {result_analysis[key][type][2]/total_user_count}\n"
            )
            fp.write(
                f"Number of Miss Touch: {result_analysis[key][type][3]/total_user_count}\n"
            )
            fp.write(
                f"Overall average delay is:{result_analysis[key][type][4]/total_user_count}\n"
            )
            fp.write(f"-------------------------------------\n\n")
        fp.write(f"==================================\n\n")
    fp.close()
