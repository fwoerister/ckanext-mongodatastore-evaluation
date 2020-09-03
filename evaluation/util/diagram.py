import matplotlib.pyplot as plt
import numpy as np


def generate_line_chart(x, data, x_label, y_label, title, ymax, target):
    for y in data:
        plt.plot(x, y)

    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.title(title)

    plt.ylim(0, ymax)

    plt.savefig(target)
    plt.show()


def generate_bar_chart(data: dict, y_label, title, x_ticks, target):
    number_of_bins = len(data.keys())

    first_label = list(data.keys())[0]
    N = len(data[first_label])
    ind = np.arange(N)
    width = 0.25

    i = 0.0
    for key in data.keys():
        plt.bar(ind + (i * width), data[key], width, label=key)
        i += 1.0

    plt.ylabel(y_label)
    plt.title(title)

    plt.xticks(ind + (width / 2) * (number_of_bins - 1), x_ticks)
    plt.legend(loc='best')
    plt.savefig(target)
    plt.show()
