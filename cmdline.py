import argparse

def main():

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

    print(args.input_dir, args.output_dir)
