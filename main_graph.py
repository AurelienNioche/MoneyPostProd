import sys
import json
from graph.graph import plot


def main(file_path, save_path):

    with open(file_path) as f:
        data = json.load(f)

    plot(data=data, save_path=save_path)

if __name__ == "__main__":

    data_path, folder_for_saving = sys.argv[1:]
    main(file_path=data_path, save_path=folder_for_saving)