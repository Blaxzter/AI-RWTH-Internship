//https://wanago.io/2018/12/10/express-mongodb-typescript-env-var/

import { model, Model, Schema } from "mongoose";
import express from "express";
import Controller from "../interfaces/controller.interface";

interface IFileServer extends Document {
  con: string;
  check_schedule: number;
  name: string;
}

const FileServerSchema = new Schema<IFileServer>({
  con: String,
  check_schedule: Number,
  name: String,
});

const FileServerModel: Model<IFileServer & Document> = model(
  "FileServer",
  FileServerSchema,
  "file_server"
);

class FileServerController implements Controller {
  public path = "/file-server";
  public router = express.Router();

  constructor() {
    this.initializeRoutes();
  }

  private initializeRoutes() {
    this.router.get(this.path, this.getAllFileServers);
  }

  private getAllFileServers = (req: express.Request, res: express.Response) => {
    FileServerModel.find().then((file_server) => {
      res.send(file_server);
    });
  };
}

export default FileServerController;
