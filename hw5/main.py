import pathlib
import argparse

from hw5 import easy_solution
def main():
    parser = argparse.ArgumentParser(description='Tool do download pictures from website')
    parser.add_argument('-n', dest='images_n', type=int, help='Number of images to download', required=True)
    parser.add_argument('-o', dest='out_dir', type=str, default='artifacts',
                        help='Directory to store downloaded images')
    args = parser.parse_args()

    images_n, out_dir = args.images_n, args.out_dir

    pathlib.Path(out_dir).mkdir(exist_ok=True)

    easy_solution(images_n, out_dir)


if __name__ == "__main__":
    main()
