import { model, Model, Schema } from "mongoose";

export interface IFileFeatures extends Document {
  name: String;
  action_date: String;
  action: String;
  user: String;
  user_difference: Number;
  frequency: Number;
  amount: Number;
  time_since_last_use: Number;
  file_server: String;
  backup_data: String;
}

export const FileFeaturesSchema = new Schema<IFileFeatures>({
  name: String,
  action_date: String,
  action: String,
  user: String,
  user_difference: Number,
  frequency: Number,
  amount: Number,
  time_since_last_use: Number,
  file_server: {
    type: Schema.Types.ObjectId,
    ref: "FileServer",
  },
  backup_data: {
    type: Schema.Types.ObjectId,
    ref: "BackupMetaData",
  },
});

export const File_featuresModel: Model<IFileFeatures & Document> = model(
  "FileFeatures",
  FileFeaturesSchema,
  "file_features"
);

export default File_featuresModel;
