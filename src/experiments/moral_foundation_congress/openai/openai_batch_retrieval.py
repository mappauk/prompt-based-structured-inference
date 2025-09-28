from openai import OpenAI
import sys
import json

def main():
    output_file_id = sys.argv[1]
    output_path = sys.argv[2]
    client = OpenAI(api_key='')
    batch_output_file = client.files.content(output_file_id).content
    with open(output_path, "wb") as json_file:
        json_file.write(batch_output_file)

if __name__ == "__main__":
    main()