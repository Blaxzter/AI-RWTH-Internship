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

file_tree_dict_name = 'file_tree'
action_data_dict_name = 'action_data'
backup_features_dict_name = 'features'
file_database_dict_name = 'file_database'
trained_features_dict_name = 'trained_features'
trained_scalers_dict_name = 'feature_scalers'

backup_date_dict_name = 'backup_date'
backup_data_dict_name = 'backup_data'
prev_backup_data_dict_name = 'prev_backup_data'

prediction_dict_name = 'prediction'
backup_metadata_dict_name = 'backup_metadata'

def feature_dict_factory():
    return dict(
        min_feature_name = 0,
        max_feature_name = 0,
        avg_feature_name = 0,
    )
