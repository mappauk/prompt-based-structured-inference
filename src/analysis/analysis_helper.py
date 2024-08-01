import json

def write_json_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def load_results(filename):
    with open(filename) as f:
        return json.load(f)  