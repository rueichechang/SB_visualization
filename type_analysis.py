import argparse
import os
import copy
from generate_analysis import generate_type_analysis

ANALYSIS_DICT = {
    "RW_FOCUS": [],
    "VR_FOCUS": [],
    "RW_PERIPHERAL": [],
    "VR_PERIPHERAL": [],
}


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", default="/json_files")
    parser.add_argument("-o", "--output", default="result.txt")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_parser()

    fp = open(args.output, "w")

    if os.path.isdir(args.input_dir):
        for scene in os.listdir(args.input_dir):
            scene_path = os.path.join(args.input_dir, scene)
            if not os.path.isdir(scene_path):
                continue
            fp.write(f"<<<<<<<<<<<<<<<<<<{scene}>>>>>>>>>>>>>>>>>>\n")
            for mode in os.listdir(scene_path):
                mode_path = os.path.join(scene_path, mode)
                if not os.path.isdir(mode_path):
                    continue
                fp.write(f"==============={mode}===============\n\n")
                analysis = copy.deepcopy(ANALYSIS_DICT)
                total_count = 0
                print("=====================")
                for logger in os.listdir(mode_path):
                    if not logger.endswith(".json"):
                        continue
                    result = generate_type_analysis(os.path.join(mode_path, logger))
                    for type in analysis:
                        if len(analysis[type]) == 0:
                            for i in range(len(result[type])):
                                analysis[type].append(result[type][i])
                        else:
                            for i in range(len(analysis[type])):
                                analysis[type][i] += result[type][i]
                    total_count += 1
                for type in analysis:
                    for i in range(len(analysis[type])):
                        analysis[type][i] = analysis[type][i] / total_count
                for type in analysis:
                    fp.write(f"---------------{type}---------------\n")
                    fp.write(f"Overall average delay is:{analysis[type][0]}\n")
                    fp.write(f"Number of Miss Event: {analysis[type][1]}\n")
                    fp.write(f"Number of Miss Touch: {analysis[type][2]}\n")
                    fp.write(f"Number of Hit Correct Event: {analysis[type][3]}\n")
                    fp.write(f"Number of Hit Error Event: {analysis[type][4]}\n")
                    fp.write(f"Total number of event is: {analysis[type][5]}\n")
                    fp.write(f"Hit Accuracy: {analysis[type][6]}\n")
                    fp.write(f"-------------------------------------\n\n")
                fp.write(f"==================================\n\n")
    fp.close()
