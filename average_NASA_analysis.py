import argparse
import os
import copy
import json
from generate_analysis import generate_result

ANALYSIS_DICT = {
    "Mental_Demand": 0,
    "Physical_Demand": 0,
    "Temporal_Demand": 0,
    "Perforamnce": 0,
    "Effort": 0,
    "Frustration": 0,
    "Overall": 0,
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
            user_path = os.path.join(os.path.join(args.input_dir, user), "NASA.json")
            if not os.path.exists(user_path):
                continue
            total_user_count += 1
            with open(user_path, "r") as json_file:
                data = json.load(json_file)
                for key in data:
                    if key not in result_analysis:
                        result_analysis[key] = copy.deepcopy(ANALYSIS_DICT)
                    for option in result_analysis[key]:
                        result_analysis[key][option] += data[key][option]

    print(total_user_count)
    for key in result_analysis:
        fp.write(f"---------------{key}---------------\n")
        for type in result_analysis[key]:
            fp.write(f"{type} : {result_analysis[key][type]/total_user_count}\n")

        fp.write(f"-------------------------------------\n\n")
        # fp.write(f"==================================\n\n")
    fp.close()
