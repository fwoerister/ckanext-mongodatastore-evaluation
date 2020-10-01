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

    input_files[testcase][tag] = {}

    with open(file) as input_file:
        line = input_file.readline()
        columns = line.split(';')

        for column in columns:
            input_files[testcase][tag][column.strip()] = []

        while line := input_file.readline():
            values = line.split(';')

            for i in range(0, len(columns)):
                input_files[testcase][tag][columns[i].strip()].append(float(values[i]))


def read_input_dir():
    input_files = {}
    for file in os.listdir(os.path.join(CHARTS_DIR, 'data')):
        load_file(os.path.join(CHARTS_DIR, 'data', file), input_files)

    return input_files


def extract_testcase_list_data(testcase, column, data_dict):
    tc_dict = data_dict[testcase]

    data = {}

    for key in tc_dict.keys():
        data[key] = tc_dict[key][column]

    return data


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
                data[column].append(float(tc_dict[label][column][0]))
            else:
                data[column].append(None)

    return labels, data


def main():
    data_dict = read_input_dir()

    data = extract_testcase_list_data('nftc1', 'filter', data_dict)
    x = numpy.arange(0.5, 9.6, step=0.5)
    generate_line_chart(x, data, '# of records (in millions)', 'response time in seconds', 'Non-Functional Test 1', 15,
                        True, os.path.join(CHARTS_DIR, 'nftc1_diagram_filter.png'))

    data = extract_testcase_list_data('nftc1', 'fulltext', data_dict)
    x = numpy.arange(0.5, 9.6, step=0.5)
    generate_line_chart(x, data, '# of records (in millions)', 'response time in seconds', 'Non-Functional Test 1', 15,
                        True, os.path.join(CHARTS_DIR, 'nftc1_diagram_fulltext.png'))

    data = extract_testcase_list_data('nftc2', 'filter', data_dict)
    x = numpy.arange(0.5, 8.6, step=0.5)
    generate_line_chart(x, data, '# of records (in millions)', 'response time in seconds', 'Non-Functional Test 2', 3,
                        False, os.path.join(CHARTS_DIR, 'nftc2_diagram_filter.png'))

    data = extract_testcase_list_data('nftc2', 'fulltext', data_dict)
    x = numpy.arange(0.5, 8.6, step=0.5)
    generate_line_chart(x, data, '# of records (in millions)', 'response time in seconds', 'Non-Functional Test 2', 3,
                        False, os.path.join(CHARTS_DIR, 'nftc2_diagram_fulltext.png'))

    labels, data = extract_testcase_dict_data('nftc3', data_dict)

    generate_bar_chart(data, 'response time in seconds', 'performance impact sharding/indexing', labels,
                       os.path.join(CHARTS_DIR, 'nftc3_diagram.png'))


if __name__ == "__main__":
    main()
