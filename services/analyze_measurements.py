import argparse
import os
import matplotlib.pyplot as plt
import json

STEP = 2

def get_json_data(file):
    with open(file) as f_json:
        data = json.load(f_json)
        first_elem = data["Spectrum"][1][0]
        plt.plot(data["Spectrum"][0], [x - first_elem for x in data["Spectrum"][1]])



def get_data_from_file(file):
    x_data = []
    y_data = []
    for i, line in enumerate(file.readlines()):
        if i == 0:
            continue
        x_data.append(float(line.split('\t')[0]))
        y_data.append(float(line.split('\t')[1]))
    return x_data, y_data


def check_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def create_dirs(path):
    for i, dir in enumerate(path.split('/')):
        check_dir('/'.join(path.split('/')[0:i+1]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=str)
    args = parser.parse_args()
    for folder in os.listdir(f"measurements/{args.folder}"):
        if os.path.isdir(f"measurements/{args.folder}/{folder}") and folder != "lamp":
            measurement_files = os.listdir(f"measurements/{args.folder}/{folder}/")
            measurement_path = f"measurements/{args.folder}/{folder}"
            for file in measurement_files:
                get_json_data(f"{measurement_path}/{file}")
    plt.show()
    # parser.add_argument('-plot', type=int)
    # args = parser.parse_args()
    # folder = args.folder
    # x_data, y_data = get_txt_data(args.folder)
    # if args.plot == 1:
    #     plt.plot(x_data, y_data)
    #     plt.show()
    # create_dirs(f"results/{folder}/lamp")
    # with open(f"results/{folder}/lamp/lamp.txt", "w+") as f:
    #     f.writelines([str(x) + "\t" + str(y_data[i]) + "\n" for i, x in enumerate(x_data)])
    # plt.show()
