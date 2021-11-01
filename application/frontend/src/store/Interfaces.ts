export interface IFileServer {
  _id: string;
  con: string;
  check_schedule: number;
  name: string;
}

export interface IBackupMetadata {
  _id: string;
  backed_up_amount: number;
  uniques_counts: {
    uniques: [string];
    counts: [number];
  };
  data_range: {
    earliest_date: number;
    latest_date: number;
  };
  date_mean_std: {
    unix_dates_mean: number;
    unix_dates_std: number;
  };
  file_server: string;
}

export interface IFileFeatures {
  _id: string;
  name: string;
  action_date: string;
  action: string;
  user: string;
  user_difference: number;
  frequency: number;
  amount: number;
  time_since_last_use: number;
  file_server: string;
  backup_data: string;
}
