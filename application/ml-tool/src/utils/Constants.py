action_index = 0
name_index = 1
user_index = 2
date_index = 3
test_file_server_name = 'test_file_server'
data_amount_per_line = 4

min_feature_name = 'min_feature'
max_feature_name = 'max_feature'
avg_feature_name = 'avg_feature'

action_rename = 'R'
action_deleted = 'D'
action_modified = 'M'
action_added = 'A'

def feature_dict_factory():
    return dict(
        min_feature_name = 0,
        max_feature_name = 0,
        avg_feature_name = 0,
    )
