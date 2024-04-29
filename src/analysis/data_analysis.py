import src.helpers.moral_prompting as moral_prompting
import src.helpers.prompt_constants as constants
import src.helpers.dataset_loader as dataset_loader
import sys
import sklearn.metrics as sk

def main():
    input_path = sys.argv[1]
    predictions, labels = dataset_loader.load_prediction_results(input_path)
    final_predictions = []
    for i in range(len(predictions)):
        templist = predictions[i][0:2]
        final_predictions.append(max(templist,key=templist.count))

    print('Macro F1:')
    print(sk.f1_score(labels, final_predictions, labels=list(constants.MORAL_FOUNDATION_DEFINITIONS_MAP.keys()), average='macro'))
    
if __name__ == "__main__":
    main()
