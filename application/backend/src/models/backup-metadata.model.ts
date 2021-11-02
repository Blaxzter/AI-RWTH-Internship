import { model, Model, Schema } from "mongoose";

export interface IBackupMetadata extends Document {
  backed_up_amount: Number;
  uniques_counts: {
    uniques: [String];
    counts: [Number];
  };
  date_range: {
    earliest_date: Number;
    latest_date: Number;
  };
  date_mean_std: {
    unix_dates_mean: Number;
    unix_dates_std: Number;
  };
  file_server: String;
}

export const BackupMetadataSchema = new Schema<IBackupMetadata>({
  backed_up_amount: Number,
  uniques_counts: {
    uniques: [String],
    counts: [Number],
  },
  date_range: {
    earliest_date: Number,
    latest_date: Number,
  },
  date_mean_std: {
    unix_dates_mean: Number,
    unix_dates_std: Number,
  },
  file_server: {
    type: Schema.Types.ObjectId,
    ref: "FileServer",
  },
});

export const BackupMetadataModel: Model<IBackupMetadata & Document> = model(
  "BackupMetaData",
  BackupMetadataSchema,
  "backup_metadata"
);

export default BackupMetadataModel;
