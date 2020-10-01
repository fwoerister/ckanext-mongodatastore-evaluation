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
        self.tag = ''
        self.results_dir = results_dir
        self.name = name
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    @abc.abstractmethod
    def run(self, tag):
        self.tag = tag


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

    def run(self, tag):
        super(GenericFunctionalTest, self).run(tag)
        self.logger.info(f"⏳ Start execution of '{self.name}'")

        self.logger.info("check preconditions...")
        self._check_precondition()
        self.logger.info("preconditions are fulfilled")

        self.logger.info("execute test steps...")
        self._execute_steps()
        self.logger.info("teststeps successfully executed")

        self.logger.info("check postconditions...")
        self._check_postcondition()
        self.logger.info("postconditions are fulfilled")

        self.logger.info(f"🎉 '{self.name}' successfully executed")


class GenericNonFunctionalTest(GenericTest, ABC):
    def __init__(self, results_dir, name, dataset, chunksize, test_interval):
        super(GenericNonFunctionalTest, self).__init__(results_dir, name)
        self._dataset = dataset
        self._chunksize = chunksize
        self._test_interval = test_interval
        self._resource_id = None
        self._random_query_generator = RandomQueryGenerator(RANDOM_SEED)

    @abc.abstractmethod
    def _prepare_preconditions(self):
        pass

    @abc.abstractmethod
    def _do_evaluation(self):
        pass

    def _get_target_resources(self):
        return [self._resource_id]

    def _after_upload(self):
        pass

    def run(self, tag):
        super(GenericNonFunctionalTest, self).run(tag)
        self.logger.info(f"⏳ Start execution of '{self.name}'")

        self.logger.info("check preconditions...")
        self._prepare_preconditions()
        self.logger.info("preconditions are fulfilled")

        with open(self._dataset) as trace_file:
            line = trace_file.readline()
            line_count = 0
            records = []
            while line:
                records.append(line_to_trace_record(line, line_count))
                line_count += 1

                if line_count % self._chunksize == 0:
                    for resource_id in self._get_target_resources():
                        response_time = timeit.timeit(
                            lambda: ckan.client.action.datastore_upsert(resource_id=resource_id, records=records,
                                                                        force=True, method='insert'), number=1)
                        with open(os.path.join(self.results_dir, 'csv', f'{self.tag}_insert_time_{resource_id}.csv'),
                                  'a') as file:
                            file.writelines(f'{response_time}\n')

                    self.logger.info(f'{str(line_count).rjust(8, " ")} records uploaded')

                    if line_count % self._test_interval == 0:
                        self.logger.info('📈 perform evaluation')
                        self._do_evaluation()
                        self.logger.info(' ✅ evaluation done')

                    records = []

                line = trace_file.readline()

            if len(records) != 0:
                for resource_id in self._get_target_resources():
                    response_time = timeit.timeit(
                        lambda: ckan.client.action.datastore_upsert(resource_id=resource_id, records=records,
                                                                    force=True, method='insert'), number=1)
                    with open(os.path.join(self.results_dir, 'csv', f'{self.tag}_insert_time_{resource_id}.csv'),
                              'a') as file:
                        file.writelines(f'{response_time}\n')

                self.logger.info(f'📈 perform evaluation - ({line_count} records uploaded)')
                self._do_evaluation()
                self.logger.info(' ✅ evaluation done')

        self._after_upload()

        self.logger.info(f"🎉 '{self.name}' successfully executed")
