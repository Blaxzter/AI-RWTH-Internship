import numpy as np
from networkx import Graph

from src.Exceptions import FeatureNotCalculated
from src.utils.Constants import name_index, min_feature_name, avg_feature_name, max_feature_name, feature_dict_factory


class PathFeatures:
    def __init__(self, path_seperator = '/', prev_backup = None):

        self.prev_backup = prev_backup
        self.path_seperator = path_seperator

        # Graph stuff
        self.root_node = 'root'
        self.file_graph = Graph()
        self.file_graph.add_node(node_for_adding = 'root')

        # Features
        self.features_calculated = False
        self.branching_factor_feature = feature_dict_factory()
        self.path_length_feature = feature_dict_factory()
        self.amount_type_endings = 0
        self.avg_file_ending_amounts = 0

    def calc_features(self, backup_data):
        # Get the paths from the feature list
        path_list = map(lambda feature: feature[name_index], backup_data)
        path_lists = map(lambda path: path.split(self.path_seperator), path_list)
        self.create_graph_representation(path_lists)
        self.count_file_endings(path_lists)
        self.features_calculated = True

    def count_file_endings(self, path_list):
        split_by_ending = map(lambda path: path[-1].split('.'), path_list)
        uniques, counts = np.unique(split_by_ending, return_counts = True)
        self.amount_type_endings = len(uniques)
        self.avg_file_ending_amounts = np.average(counts)

    def create_graph_representation(self, paths_lists):
        length_list = []
        for path_list in paths_lists:

            if len(path_list[0]) == 0:
                path_list.pop(0)

            # Add the avg length feature
            length_list.append(len(path_list))

            prev_node = self.root_node

            # Create path graph
            for index in range(1, len(path_list) + 1):
                # The node id is always the whole prev path to allow folders with the same name in different locations
                next_node_id = '/'.join(path_list[:index])
                self.file_graph.add_node(next_node_id)
                self.file_graph.add_edge(prev_node, next_node_id)

                # Set next prev node
                prev_node = next_node_id

        # Calc the graph features
        branching_list = list(map(lambda node: len(self.file_graph[node]) - 1, self.file_graph.nodes()))
        self.branching_factor_feature[avg_feature_name] = np.average(branching_list)
        self.branching_factor_feature[min_feature_name] = np.min(branching_list)
        self.branching_factor_feature[max_feature_name] = np.max(branching_list)

        self.path_length_feature[avg_feature_name] = np.average(length_list)
        self.path_length_feature[min_feature_name] = np.min(length_list)
        self.path_length_feature[max_feature_name] = np.max(length_list)

    def get_avg_path_length_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The avg path length feature is not calculated. Pls. call calc_features first')
        return self.path_length_feature[avg_feature_name]

    def get_min_path_length_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The min path length feature is not calculated. Pls. call calc_features first')
        return self.path_length_feature[min_feature_name]

    def get_max_path_length_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated('The max path length feature is not calculated. Pls. call calc_features first')
        return self.path_length_feature[max_feature_name]

    def get_avg_branching_factor_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated(
                'The avg branching factor feature is not calculated. Pls. call calc_features first')
        return self.branching_factor_feature[avg_feature_name]

    def get_min_branching_factor_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated(
                'The min branching factor feature is not calculated. Pls. call calc_features first')
        return self.branching_factor_feature[min_feature_name]

    def get_max_branching_factor_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated(
                'The max branching factor feature is not calculated. Pls. call calc_features first')
        return self.branching_factor_feature[max_feature_name]
