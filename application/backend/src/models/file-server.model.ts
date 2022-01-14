import { model, Model, Schema } from "mongoose";

export interface IFileServer extends Document {
  con: string;
  check_schedule: string;
  name: string;
}

export const FileServerSchema = new Schema<IFileServer>({
  con: String,
  check_schedule: String,
  name: String
});

export const FileServerModel: Model<IFileServer & Document> = model(
  "FileServer",
  FileServerSchema,
  "file_server"
);

export default FileServerModel;
