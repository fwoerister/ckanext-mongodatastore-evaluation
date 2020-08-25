import hashlib
import json

HASH_ALGORITHM = hashlib.md5


def calculate_hash(data):
    algo = HASH_ALGORITHM()

    if type(data) == str:
        algo.update(data)
    elif type(data) == dict:
        algo.update(json.dumps(data, default=str, sort_keys=True).encode('utf-8'))
    elif type(data) == list:
        for doc in data:
            algo.update(json.dumps(doc, default=str, sort_keys=True).encode('utf-8'))

    return algo.hexdigest()


def calculate_hash_of_file(file):
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def verify_hash(obj, expected_hash):
    hash = calculate_hash(obj['records'])
    assert hash == expected_hash, f"Expected the hash value to be {expected_hash} but was {hash}"


def verify_all_elements_have_same_hash(values, hash_func):
    results = values(map(lambda result: hash_func(result), values))
    assert all(result_hash == results[0] for result_hash in results)
