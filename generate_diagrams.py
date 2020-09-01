import os

import numpy

from evaluation.util.diagram import generate_line_chart, generate_bar_chart

CHARTS_DIR = './charts'


def load_file(file, input_files):
    filename = os.path.basename(file)
    tag = filename.split('_')[0]
    testcase = filename.split('_')[1]

    if testcase not in input_files.keys():
        input_files[testcase] = {}

    input_files[testcase][tag] = []

    with open(file) as input_file:
        line = input_file.readline()
        columns = None
        if line.count(';') > 0:
            columns = line.split(';')

        while line := input_file.readline():
            if columns:
                values = line.split(';')
                input_files[testcase][tag] = {}
                for i in range(0, len(columns)):
                    input_files[testcase][tag][columns[i].strip()] = float(values[0])

            else:
                input_files[testcase][tag].append(float(line))


def read_input_dir():
    input_files = {}
    for file in os.listdir(os.path.join(CHARTS_DIR, 'data')):
        load_file(os.path.join(CHARTS_DIR, 'data', file), input_files)

    return input_files


def extract_testcase_list_data(testcase, column, data_dict):
    tc_dict = data_dict[testcase]

    data = []
    labels = []

    for key in tc_dict.keys():
        data.append(tc_dict[key])
        labels.append(key)

    return labels, data


def extract_testcase_dict_data(testcase, data_dict):
    tc_dict = data_dict[testcase]
    labels = []
    data = {}
    columns = set()
    for tag in tc_dict.keys():
        labels.append(tag)
        columns = columns.union(tc_dict[tag].keys())

    labels.sort()

    for column in columns:
        data[column] = []

    for label in labels:
        for column in columns:
            if column in tc_dict[label].keys():
                data[column].append(float(tc_dict[label][column]))
            else:
                data[column].append(None)

    return labels, data


def main():
    data_dict = read_input_dir()

    label, data = extract_testcase_list_data('nftc1', 'filter', data_dict)
    x = numpy.arange(len(data[0])) + 1
    generate_line_chart(x, data, '# of records (in millions)', 'response time in seconds', 'Non-Functional Test 1',
                        os.path.join(CHARTS_DIR, 'nftc1_diagram.png'))

    label, data = extract_testcase_list_data('nftc1', 'fulltext', data_dict)
    x = numpy.arange(len(data[0])) + 1
    generate_line_chart(x, data, '# of records (in millions)', 'response time in seconds', 'Non-Functional Test 1',
                        os.path.join(CHARTS_DIR, 'nftc1_diagram.png'))

    label, data = extract_testcase_list_data('nftc2', data_dict)
    x = numpy.arange(len(data[0])) + 1
    generate_line_chart(x, data, '# of records (in millions)', 'response time in seconds', 'Non-Functional Test 2',
                        os.path.join(CHARTS_DIR, 'nftc2_diagram.png'))

    labels, data = extract_testcase_dict_data('nftc3', data_dict)

    generate_bar_chart(data, 'response time in seconds', 'performance impact sharding/indexing', labels, os.path.join(CHARTS_DIR, 'nftc3_diagram.png'))


if __name__ == "__main__":
    main()
