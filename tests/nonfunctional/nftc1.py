import logging
import timeit

# DESCRIPTION
#


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logging.info("Start execution of 'nftc1'")

# PRE-REQUISIT

# STEPS
with open(DATASET, 'r') as trace_file:
    with open(OUTPUT + 'insert_time.csv', 'a') as f:
        f.writelines('{0}:\n'.format(DATASET))
        line = trace_file.readline()
        line_count = 0
        records = []
        while line:
            records.append(line_to_trace_record(line, line_count))
            line_count += 1

            if line_count % CHUNK_SIZE == 0:
                response_time = timeit.timeit(
                    lambda: client.action.datastore_upsert(resource_id=trace_resource['id'], records=records,
                                                           force=True,
                                                           method='insert'), number=1)
                f.writelines('{0}\n'.format(response_time))
                f.flush()
                print('uploaded {0} records, total: {1}'.format(len(records), line_count))
                records = []

                if line_count in [100000, 1000000]:
                    perform_evaluation(str(line_count))

            line = trace_file.readline()

        if len(records) != 0:
            response_time = timeit.timeit(
                lambda: client.action.datastore_upsert(resource_id=trace_resource['id'], records=records,
                                                       force=True,
                                                       method='insert'), number=1)
            f.writelines('{0}\n'.format(response_time))
            print('uploaded {0} records, total: {1}'.format(len(records), line_count))



# EXPECTED RESULTS