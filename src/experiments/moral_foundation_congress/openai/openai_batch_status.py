from openai import OpenAI
import sys
import json

def main():
    input_file = sys.argv[1]
    data = None
    with open(input_file, "r") as json_file:
        data = json.load(json_file)
    batch_id = data['batch_id']
    client = OpenAI(api_key='')
    batch_info = client.batches.retrieve(batch_id)
    print(batch_info)

if __name__ == "__main__":
    main()