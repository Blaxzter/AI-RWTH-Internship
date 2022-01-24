import pickle
from collections import defaultdict

if __name__ == '__main__':

    with open('data/re_predict_data.pickle', 'rb') as handle:
        re_predict_data = pickle.load(handle)

    with open('data/prediction.pickle', 'rb') as handle:
        predictions = pickle.load(handle)

    total_outlier_detected = defaultdict(int)
    classified_the_same_positive = defaultdict(int)
    classified_the_same_negative = defaultdict(int)
    different_classification = defaultdict(int)

    for model_name in predictions.keys():
        for idx, re_prediciton in enumerate(re_predict_data[model_name][-1][0]):
            continues_prediction = predictions[model_name][idx]['prediction']
            if continues_prediction is None:
                continue

            total_outlier_detected[f'{model_name}_re-prediction'] += re_prediciton
            total_outlier_detected[f'{model_name}_continues-prediction'] += continues_prediction

            if re_prediciton == continues_prediction:
                if re_prediciton == 1:
                    classified_the_same_positive[f'{model_name}_re-vs-predict'] += 1
                else:
                    classified_the_same_negative[f'{model_name}_re-vs-predict'] += 1
            else:
                different_classification[f'{model_name}_re-vs-predict'] += 1

    for idx in range(len(predictions['path_ocsvm'])):
        ocsvm_prediction = predictions['path_ocsvm'][idx]['prediction']
        suod_prediction = predictions['meta_data_model'][idx]['prediction']

        if ocsvm_prediction == suod_prediction:
            if ocsvm_prediction == 1:
                classified_the_same_positive[f'continues_path_ocsvm_vs_meta_data_model'] += 1
            else:
                classified_the_same_negative[f'continues_path_ocsvm_vs_meta_data_model'] += 1
        else:
            different_classification[f'continues_path_ocsvm_vs_meta_data_model'] += 1

    for idx in range(len(predictions['path_ocsvm'])):
        ocsvm_prediction = re_predict_data['path_ocsvm'][-1][0][idx]
        suod_prediction = re_predict_data['meta_data_model'][-1][0][idx]

        if ocsvm_prediction == suod_prediction:
            if ocsvm_prediction == 1:
                classified_the_same_positive[f're_prediction_ocsvm_vs_meta_data_model'] += 1
            else:
                classified_the_same_negative[f're_prediction_path_ocsvm_vs_meta_data_model'] += 1
        else:
            different_classification[f're_prediction_path_ocsvm_vs_meta_data_model'] += 1

    print(f'total_outlier_detected {total_outlier_detected}\n',
          f'classified_the_same_positive {classified_the_same_positive}\n',
          f'classified_the_same_negative {classified_the_same_negative}\n',
          f'different_classification {different_classification}\n')
