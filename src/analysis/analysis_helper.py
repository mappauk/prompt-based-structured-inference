import json
import os

def write_json_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def load_results(filename):
    with open(filename) as f:
        return json.load(f)
    
def load_multiple_results(path):
    results = []
    if path.find('.json') > 0:
        with open(path) as f:
            return [{
                'name': f.name,
                'content': json.load(f)
            }]
    else:
        for root, dirs, files in os.walk(path):
            for file in files:
                with open(os.path.join(root, file)) as f:
                    results.append({
                        'name': f.name,
                        'content': json.load(f)
                    })
        return results