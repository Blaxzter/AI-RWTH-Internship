import time

import dateutil.parser
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from src.Exceptions import FeatureNotCalculated
from src.utils import Constants


class DateFeatures:
    def __init__(self):
        # Features
        self.start_time = None
        self.end_time = None
        self.time_range = None
        self.time_standard_deviation = None
        self.time_avg = None

        # Utils
        self.unix_date_scaler = MinMaxScaler()
        self.features_calculated = False

    def get_feature_list(self) -> dict:
        return dict(
            # Date Feature (Subtracted date day from days)
            start_time = self.get_start_time_feature,
            end_time = self.get_end_time_feature,
            time_range = self.get_time_range_feature,
            time_standard_deviation = self.get_time_standard_deviation_feature,
            time_avg = self.get_time_avg_feature,
        )

    def calc_features(self, backup_data):
        # Parse every date to an date object
        access_dates_list = list(
            map(lambda backup_element:
                dateutil.parser.parse(backup_element[Constants.date_index]),
                backup_data)
        )
        current_date = time.mktime(access_dates_list[0].date().timetuple())

        # Create an unix time stamp numpy array
        unix_dates = np.array(list(map(lambda date: time.mktime(date.timetuple()), access_dates_list)))
        unix_dates = unix_dates - current_date

        self.start_time = unix_dates.min()
        self.end_time = unix_dates.max()

        self.time_range = self.end_time - self.start_time

        # Get the mean and std deviation of the min max scaled date range of all changes
        unix_dates = unix_dates.reshape(-1, 1)
        unix_dates_scaled = self.unix_date_scaler.fit_transform(unix_dates)

        self.time_avg = np.mean(unix_dates_scaled)
        self.time_standard_deviation = np.std(unix_dates_scaled)
        self.features_calculated = True

    def get_start_time_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The start time feature is not calculated. Pls. call calc_features first')
        return self.start_time.item()

    def get_end_time_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The end time feature is not calculated. Pls. call calc_features first')
        return self.end_time.item()

    def get_time_range_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The time range feature is not calculated. Pls. call calc_features first')
        return self.time_range.item()

    def get_time_standard_deviation_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The time standard deviation feature is not calculated. Pls. call calc_features first')
        return self.time_standard_deviation.item()

    def get_time_avg_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The time average is not calculated. Pls. call calc_features first')
        return self.time_avg.item()
