import { model, Model, Schema } from "mongoose";

export interface IBackupMetadata extends Document {
  backup_date: Number;
  predictions: Array<Object>;
  features: Object;
  action_data: Object;
  file_server: String;
}

export const BackupMetadataSchema = new Schema<IBackupMetadata>({
  backup_date: Number,
  predictions: Array,
  features: Object,
  action_data: Object,
  file_server: {
    type: Schema.Types.ObjectId,
    ref: "FileServer"
  }
});

export const BackupMetadataModel: Model<IBackupMetadata & Document> = model(
  "BackupMetaData",
  BackupMetadataSchema,
  "backup_metadata"
);

export default BackupMetadataModel;
