import argparse
import os
import matplotlib.pyplot as plt

STEP = 2

FILES = [
    "350-1100.txt",
    "350-1100_ks-10.txt",
    "900-1500_ks-10.txt",
    ]


def get_data_from_file(file):
    x_data = []
    y_data = []
    for i, line in enumerate(file.readlines()):
        if i == 0:
            continue
        x_data.append(float(line.split('\t')[0]))
        y_data.append(float(line.split('\t')[1]))
    return x_data, y_data


def get_txt_data(folder_name):
    data_files = os.listdir(f"measurements/{folder_name}/lamp")
    tot_spectra = []
    for file in FILES:
        with open(f"measurements/{folder_name}/lamp/{file}") as f_txt:
            if file == "350-1100.txt":
                x_data, y_data = get_data_from_file(f_txt)
            if file == "350-1100_ks-10.txt":
                x_data_tmp, y_data_tmp = get_data_from_file(f_txt)
                x_data = x_data[0:151] + x_data_tmp[151:]
                y_data = y_data[0:151] + [
                    elem * y_data[-225] / y_data_tmp[151] for elem in y_data_tmp[151:]
                ]
            if file == "900-1500_ks-10.txt":
                x_data_tmp, y_data_tmp = get_data_from_file(f_txt)
                x_data = x_data[0:-50] + x_data_tmp[51:]
                y_data = y_data[0:-50] + [
                    elem * y_data[-50] / y_data_tmp[51] for elem in y_data_tmp[51:]
                ]
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
    parser.add_argument('-plot', type=int)
    args = parser.parse_args()
    folder = args.folder
    x_data, y_data = get_txt_data(args.folder)
    if args.plot == 1:
        plt.plot(x_data, y_data)
        plt.show()
    create_dirs(f"results/{folder}/lamp")
    with open(f"results/{folder}/lamp/lamp.txt", "w+") as f:
        f.writelines([str(x) + "\t" + str(y_data[i]) + "\n" for i, x in enumerate(x_data)])
    plt.show()
