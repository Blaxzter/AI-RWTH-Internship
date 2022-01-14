export interface IFileServer {
  _id: string;
  con: string;
  check_schedule: string;
  name: string;
}

export interface IBackupMetadata {
  _id: string;
  backup_date: number;
  predictions: unknown;
  features: unknown;
  action_data: unknown;
  file_server_id: string;
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
