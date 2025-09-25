from openai import OpenAI
import sys
import json

def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    client = OpenAI(api_key='')
    batch_input_file = client.files.create(
        file=open(input_path, "rb"),
        purpose="batch"
    )
    print(batch_input_file)
    batch = client.batches.create(
        input_file_id=batch_input_file.id,
        endpoint="/v1/chat/completions",
        completion_window='24h',
    )
    print(batch)
    batch_output = {
        "file_id": batch['input_file_id'],
        "batch_id": batch['id']
    }
    with open(output_path, "w") as json_file:
        json.dump(batch, json_file)

if __name__ == "__main__":
    main()