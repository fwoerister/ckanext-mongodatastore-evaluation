import os
import random

FILTER_VAL_DIR = 'data/datasets/filter_values'


def line_to_trace_record(line, identifier):
    splitted_line = line.split(' ')
    return {
        'id': identifier,
        'sent': splitted_line[0].strip(),
        'first_received': splitted_line[1].strip(),
        'last_received': splitted_line[2].strip(),
        'client_ip': splitted_line[3].strip(),
        'server_ip': splitted_line[4].strip(),
        'client_port': int(splitted_line[5]),
        'server_port': int(splitted_line[6]),
        'client_headers': splitted_line[7].strip(),
        'server_headers': splitted_line[8].strip(),
        'modified_expires_headers': splitted_line[9].strip(),
        'http_response_header_length': splitted_line[10],
        'response_data_length': splitted_line[11],
        'request_url_length': splitted_line[12],
        'request_url': ' '.join(splitted_line[13:]).strip()
    }


class RandomQueryGenerator:
    def __init__(self):
        self.value_dict = dict()
        for filename in os.listdir(FILTER_VAL_DIR):
            self.value_dict[self.__strip_filename(filename)] = []
            with open(os.path.join(FILTER_VAL_DIR, filename), 'r') as value_file:
                val = value_file.readline().rstrip()
                if filename.startswith('int'):
                    val = int(val)
                self.value_dict[self.__strip_filename(filename)].append(val)

    @staticmethod
    def __strip_filename(filename):
        parts = filename.split('_')
        return '_'.join(parts[1:])

    def generate_random_queries(self, size=1, seed=1):
        queries = []
        random.seed(seed)

        for i in range(0, size):
            queries.append(self._generate_random_query())

        return queries

    def _generate_random_query(self, number_of_fields=4):
        query = {}

        for i in range(0, number_of_fields):
            field = random.choice(list(self.value_dict.keys()))
            filter_value = random.choice(self.value_dict[field])
            query.update({field, filter_value})

        return query
