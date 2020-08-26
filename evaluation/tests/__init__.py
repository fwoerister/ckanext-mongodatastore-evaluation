import abc
import logging
import os
import timeit
from abc import ABC

from evaluation.util import ckan as ckan
from evaluation.util.trace import line_to_trace_record, RandomQueryGenerator

RANDOM_SEED = 1234


class GenericTest(ABC):
    def __init__(self, results_dir, name):
        self.results_dir = results_dir
        self.name = name
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    @abc.abstractmethod
    def run(self):
        pass


class GenericFunctionalTest(GenericTest, ABC):
    def __init__(self, results_dir, name):
        super(GenericFunctionalTest, self).__init__(results_dir, name)
        logging.basicConfig(level=logging.INFO)

    @abc.abstractmethod
    def _check_precondition(self):
        self.logger.debug("start checking precondition")
        pass

    @abc.abstractmethod
    def _execute_steps(self):
        pass

    @abc.abstractmethod
    def _check_postcondition(self):
        pass

    def run(self):
        self.logger.info(f"⏳ Start execution of '{self.name}' ⏳ ")

        self.logger.info("check preconditions...")
        self._check_precondition()
        self.logger.info("preconditions are fulfilled")

        self.logger.info("execute test steps...")
        self._execute_steps()
        self.logger.info("teststeps successfully executed")

        self.logger.info("check postconditions...")
        self._check_postcondition()
        self.logger.info("postconditions are fulfilled")

        self.logger.info(f"🎉 🎉 🎉 '{self.name}' successfully executed 🎉 🎉 🎉")


class GenericNonFunctionalTest(GenericTest, ABC):
    def __init__(self, results_dir, name, dataset, chunksize):
        super(GenericNonFunctionalTest, self).__init__(results_dir, name)
        self._dataset = dataset
        self._chunksize = chunksize
        self._resource_id = None
        self._random_query_generator = RandomQueryGenerator(RANDOM_SEED)

    @abc.abstractmethod
    def _prepare_preconditions(self):
        pass

    @abc.abstractmethod
    def _do_evaluation(self):
        pass

    def run(self):
        self.logger.info(f"⏳ Start execution of '{self.name}' ⏳ ")

        self.logger.info("check preconditions...")
        self._prepare_preconditions()
        self.logger.info("preconditions are fulfilled")


        with open(self._dataset) as trace_file:
            with open(os.path.join(self.results_dir, 'csv', 'insert_time.csv'), 'w') as insert_time_file:
                line = trace_file.readline()
                line_count = 0
                records = []
                while line:
                    records.append(line_to_trace_record(line, line_count))
                    line_count += 1

                    if line_count % self._chunksize == 0:
                        response_time = timeit.timeit(
                            lambda: ckan.client.action.datastore_upsert(resource_id=self._resource_id, records=records,
                                                                        force=True, method='insert'), number=1)
                        insert_time_file.writelines(f'{response_time}\n')
                        insert_time_file.flush()

                        self.logger.info(f'📈 perform evaluation - ({line_count} records uploaded) 📈 ')
                        self._do_evaluation()

                        records = []

                    line = trace_file.readline()

                if len(records) != 0:
                    response_time = timeit.timeit(
                        lambda: ckan.client.action.datastore_upsert(resource_id=self._resource_id, records=records,
                                                                    force=True, method='insert'), number=1)
                    insert_time_file.writelines('{0}\n'.format(response_time))

                    self.logger.info(f'📈 perform evaluation - ({line_count} records uploaded) 📈 ')
                    self._do_evaluation()

        self.logger.info(f"🎉 '{self.name}' successfully executed 🎉 ")
