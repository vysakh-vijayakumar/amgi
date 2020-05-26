import re
import sys
import os
import json
import argparse

def load_json(filename):
    with open(filename) as file:
        medias = json.load(file)
    return medias


def make_cfg(input_cfg_file, timecode):
    with open(input_cfg_file) as file:
        content = file.read()

    pattern = r'RecutMoveTC=\d{2}:\d{2}:\d{2}:\d{2}'
    repl = "RecutMoveTC=" + timecode

    replaced = re.sub(pattern, repl, content)

    with open("ez_output.cfg", "w") as file:
        file.write(replaced)


def main():
    print("main is called")
    json_path = "media.json"
    medias = load_json(json_path)

    ap = argparse.ArgumentParser(
        description='Process Moonbug jobs',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    ap.add_argument(
        '-i', '--input',
        help='input directory',
        dest='input_dir',
        required=True)

    ap.add_argument(
        '-o', '--output',
        help='output directory',
        dest='output_dir',
        required=True)

    args = ap.parse_args()

    path = args.input_dir
    files = os.listdir(path)

    for file in files:
       _, filename = os.path.split(file)
       title, ext = os.path.splitext(filename)
       asset_id = title.replace("_ENG", "")
       for media in medias["media"]:
           if asset_id == media["asset_id"]:
                json_timecode = media["tc_in"]
                make_cfg("ez_input.cfg",json_timecode)
                cfg_path = "ez_output.cfg"
                output_filename = title + ext
                output_path = os.path.join(args.output_dir, output_filename)
                command = "ezc5c -c {} -i scc -o scc {} {}".format(
                    cfg_path, filename, output_path)
                print(command)
                os.system(command)

if __name__ == "__main___":
    main()
            
