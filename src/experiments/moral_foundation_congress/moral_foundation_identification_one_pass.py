import src.helpers.moral_prompting as moral_prompting
import src.helpers.dataset_loader as dataset_loader
import sys

def main():
    #epochs = 2
    #batch_size = 2
    #return_sequences = 2
    batch_size = 16
    epochs = 5
    return_sequences = 2
    temperature = 0.5
    topk = 5

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    # load dataset
    ids, tweets, labels = dataset_loader.load_dataset_foundation_identification(input_path)
    # load model
    model, tokenizer = moral_prompting.load_mixtral_model()
    # tokenize dataset
    prompts = []
    batched_inputs = []
    for tweet in tweets:
        prompt = moral_prompting.generate_moral_foundation_identification_prompt_one_pass(tweet)
        prompts.append(prompt)
    for i in range(0, len(prompts), batch_size):
        inputs = tokenizer(prompts[i: min(i + batch_size, len(prompts))], padding=True, return_tensors='pt').to('cuda')
        batched_inputs.append(inputs)
    predictions = {}
    for i in range(epochs):
        current_index = 0
        # prompt dataset
        for j in range(len(batched_inputs)):
            outputs = model.generate(**batched_inputs[j], max_new_tokens=10, do_sample=True, top_k=topk, temperature=temperature, num_return_sequences=return_sequences, pad_token_id=tokenizer.eos_token_id)
            text_outputs = tokenizer.batch_decode(outputs[:, batched_inputs[j].input_ids.shape[1] - 1:])
            for k in range(int(len(text_outputs)/return_sequences)):
                example_predictions = []
                for l in range(return_sequences):
                    next_output = text_outputs[k*return_sequences + l]
                    example_predictions.append(moral_prompting.extract_moral_foundation_label(next_output))
                if i == 0:
                    batch_predictions = {}
                    batch_predictions['predicted_labels'] = example_predictions
                    predictions[ids[current_index]] = batch_predictions
                    batch_predictions['true_label'] = labels[current_index]
                else:
                    predictions[ids[current_index]]['predicted_labels'] = predictions[ids[current_index]]['predicted_labels'] + example_predictions
                current_index += 1
            predictions['last_updated_index'] = current_index - 1
            predictions['last_updated_epoch'] = i        
        dataset_loader.write_json_file(output_path, predictions)
if __name__ == "__main__":
    main()

