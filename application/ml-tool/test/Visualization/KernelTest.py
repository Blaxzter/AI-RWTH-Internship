import pickle
from collections import defaultdict

import numpy as np

if __name__ == '__main__':
    with open('data/re_predict_data.pickle', 'rb') as handle:
        re_predict_data = pickle.load(handle)

    with open('data/one_prediction.pickle', 'rb') as handle:
        predictions = pickle.load(handle)

    total_outlier_detected = defaultdict(int)
    classified_the_same_positive = defaultdict(int)
    classified_the_same_negative = defaultdict(int)
    different_classification = defaultdict(int)

    original_predictions = re_predict_data['path_ocsvm'][-1][0]
    normalized_predictions = predictions['path_ocsvm'][0]

    same_positive = []
    same_negative = []
    different = []

    for idx, original_prediction in enumerate(original_predictions):
        normalized_prediction = normalized_predictions[idx]

        total_outlier_detected[f'Original'] += original_prediction
        total_outlier_detected[f'normalized_prediction'] += normalized_prediction

        if original_prediction == normalized_prediction:
            if original_prediction == 1:
                classified_the_same_positive[f'Original-vs-Normalized'] += 1
                same_positive.append(idx)
            else:
                classified_the_same_negative[f'Original-vs-Normalized'] += 1
                same_negative.append(idx)
        else:
            different_classification[f'Original-vs-Normalized'] += 1
            different.append(idx)

    different_confidence_original = np.asarray(re_predict_data['path_ocsvm'][-1][1])[different]
    different_confidence_normalized = np.asarray(predictions['path_ocsvm'][1])[different]
    same_positive_confidence_original = np.asarray(re_predict_data['path_ocsvm'][-1][1])[same_positive]
    same_positive_confidence_normalized = np.asarray(predictions['path_ocsvm'][1])[same_positive]
    same_negative_confidence_original = np.asarray(re_predict_data['path_ocsvm'][-1][1])[same_negative]
    same_negative_confidence_normalized = np.asarray(predictions['path_ocsvm'][1])[same_negative]

    print(
        'different_confidence_original', np.average(different_confidence_original), '\n'
        'different_confidence_normalized', np.average(different_confidence_normalized), '\n'
        'same_positive_confidence_original', np.average(same_positive_confidence_original), '\n'
        'same_positive_confidence_normalized', np.average(same_positive_confidence_normalized), '\n'
        'same_negative_confidence_original', np.average(same_negative_confidence_original), '\n'
        'same_negative_confidence_normalized', np.average(same_negative_confidence_normalized), '\n'
    )

    print("total_outlier_detected", total_outlier_detected, "\n",
          "classified_the_same_positive", classified_the_same_positive, "\n",
          "classified_the_same_negative", classified_the_same_negative, "\n",
          "different_classification", different_classification, "\n")
