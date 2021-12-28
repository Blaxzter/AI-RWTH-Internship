import numpy as np
from networkx import Graph

from src.Exceptions import FeatureNotCalculated
from src.od.metadata_features.IFeatureExtractor import IFeatureExtractor
from src.od.searchutils.FileTreeDatabase import FileTreeDatabase
from src.utils.Constants import name_index, min_feature_name, avg_feature_name, max_feature_name, feature_dict_factory


class PathFeatures(IFeatureExtractor):
    def __init__(self, prev_backup: FileTreeDatabase = None, data_base: FileTreeDatabase = None, path_separator = '/'):

        super().__init__()
        self.prev_backup = prev_backup
        self.path_separator = path_separator
        self.data_base = data_base

        # Graph stuff
        self.root_node = 'root'
        self.file_graph = Graph()
        self.file_graph.add_node(node_for_adding = 'root')

        # Features
        self.branching_factor_feature = feature_dict_factory()
        self.path_length_feature = feature_dict_factory()

        self.amount_type_endings = 0
        self.avg_file_ending_amounts = 0
        self.amount_not_previously_stored = 0
        self.cross_section = 0
        self.diff_folders_amount = 0

    def get_feature_list(self) -> dict:
        return dict(
            # Path features
            min_path_length = self.get_min_path_length_feature,
            max_path_length = self.get_max_path_length_feature,
            avg_path_length = self.get_avg_path_length_feature,
            min_branching_factor = self.get_min_branching_factor_feature,
            max_branching_factor = self.get_max_branching_factor_feature,
            avg_branching_factor = self.get_avg_branching_factor_feature,

            # Folder / Files
            diff_folders_amount = self.get_diff_folders_amount_feature,
            amount_type_endings = self.get_amount_type_endings_feature,
            avg_file_ending_amounts = self.get_avg_file_ending_amounts_feature,
            amount_not_previously_stored = self.get_amount_not_previously_stored_feature,
            cross_section = self.get_cross_section_feature,
        )

    def calc_features(self, backup_data):
        # Get the paths from the feature list
        path_list = list(map(lambda feature: feature[name_index], backup_data))
        path_lists = list(map(lambda path: path.split(self.path_separator), path_list))

        self.create_graph_representation(path_lists)
        self.count_file_endings(path_lists)
        self.not_previously_stored(path_list)
        self.features_calculated = True

    def cross_section(self, path_list):
        for path in path_list:
            if path in self.prev_backup:
                self.cross_section += 1

    def not_previously_stored(self, path_list):
        for element in path_list:
            if element not in self.data_base:
                self.amount_not_previously_stored += 1

    def count_file_endings(self, path_lists):
        split_by_ending = list(map(lambda path: path[-1].split('.')[-1], path_lists))
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

        # TODO Currently it counts the folder amount
        # Count diff folders by going over each note and counting if it has children (beeing a folder)
        self.diff_folders_amount = sum(
            map(lambda node: 0 if len(self.file_graph[node]) == 0 else 1, self.file_graph.nodes()))

        # Calc the graph metadata_features
        branching_list = np.asarray(list(map(lambda node: len(self.file_graph[node]) - 1, self.file_graph.nodes())))
        branching_list_no_folders = branching_list[np.where(branching_list != 0)]
        self.branching_factor_feature[avg_feature_name] = np.average(branching_list_no_folders)
        self.branching_factor_feature[min_feature_name] = np.min(branching_list_no_folders)
        self.branching_factor_feature[max_feature_name] = np.max(branching_list_no_folders)

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

    def get_amount_type_endings_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated(
                'the amount_type_endings feature is not calculated. Pls. call calc_features first'
            )
        return self.amount_type_endings

    def get_avg_file_ending_amounts_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated(
                'the avg_file_ending_amounts feature is not calculated. Pls. call calc_features first'
            )
        return self.avg_file_ending_amounts

    def get_amount_not_previously_stored_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated(
                'the amount_not_previously_stored feature is not calculated. Pls. call calc_features first'
            )
        return self.amount_not_previously_stored

    def get_cross_section_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated(
                'the cross section feature is not calculated. Pls. call calc_features first'
            )
        return self.cross_section

    def get_diff_folders_amount_feature(self):
        if self.features_calculated is False:
            raise FeatureNotCalculated(
                'the diff folders amount feature is not calculated. Pls. call calc_features first'
            )
        return self.diff_folders_amount

