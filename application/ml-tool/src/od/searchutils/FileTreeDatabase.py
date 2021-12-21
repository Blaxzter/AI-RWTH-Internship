from typing import Optional

from anytree import Node
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter

from src.utils import Constants


class FileTreeDatabase:
    def __init__(self, backup_data = None, path_separator = '/', add_user = False):
        self.path_separator = path_separator
        self.add_user = add_user

        self.size = 0

        self.root_node = Node('root')

        if backup_data is not None:
            self.add_backup_data(backup_data)
            return

    def add_backup_data(self, backup_data):
        for backup_instance in backup_data:
            self.add_backup_instance(backup_instance)

    def add_backup_instance(self, backup_instance):
        path = backup_instance[Constants.name_index]
        path_list = path.split(self.path_separator)

        prev_node = self.root_node

        new_node = False

        # Create path graph
        for index in range(0, len(path_list)):

            next_path_element = path_list[index]
            try:
                # Check if element is already present and add if not
                child_idx = list(map(lambda node: node.name, prev_node.children)).index(next_path_element)
                next_node = prev_node.children[child_idx]
            except ValueError:
                new_node = True
                next_node = Node(next_path_element, parent = prev_node)

            # Set next prev node
            prev_node = next_node

        if new_node:
            self.size += 1

        if self.add_user and new_node:
            prev_node.user = backup_instance[Constants.user_index]

    def get_storable_elements(self):
        exporter = JsonExporter()
        return exporter.export(self.root_node)

    def load_from_string(self, file_tree):
        importer = JsonImporter()
        self.root_node = importer.import_(file_tree)

    def __getitem__(self, file_path: str) -> Optional[Node]:
        split_file_path = file_path.split(self.path_separator)

        current_node = self.root_node
        # Go over each element of the path
        for elem_idx in range(len(split_file_path)):

            found_idx = -1

            #  and check if the element is on the current tree level
            for idx, child in enumerate(current_node.children):
                if child.name == split_file_path[elem_idx]:
                    found_idx = idx
                    break

            if found_idx == -1:
                return None

            current_node = current_node.children[found_idx]

        return current_node

    def __contains__(self, file_path: str):
        split_file_path = file_path.split(self.path_separator)

        current_node = self.root_node
        # Go over each element of the path
        for elem_idx in range(len(split_file_path)):

            found_idx = -1

            #  and check if the element is on the current tree level
            for idx, child in enumerate(current_node.children):
                if child.name == split_file_path[elem_idx]:
                    found_idx = idx
                    break

            if found_idx == -1:
                return False

            current_node = current_node.children[found_idx]

        return True
