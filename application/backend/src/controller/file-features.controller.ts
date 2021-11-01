//https://wanago.io/2018/12/10/express-mongodb-typescript-env-var/

import express from "express";
import Controller from "../interfaces/controller.interface";
import {
  File_featuresModel,
  IFileFeatures,
} from "../models/file_features.model";

class FileFeaturesController implements Controller {
  public path = "/file-features";
  public router = express.Router();

  constructor() {
    this.initializeRoutes();
  }

  private initializeRoutes() {
    this.router.get(this.path, this.getFileFeatures);
    this.router.get(`${this.path}/:id`, this.getFileFeaturesById);
  }

  private getFileFeatures = (req: express.Request, res: express.Response) => {
    console.log(`Invoked: getFileFeatures query ${JSON.stringify(req.query)}`);
    File_featuresModel.find(req.query).then((file_server) => {
      res.send(file_server);
    });
  };

  private getFileFeaturesById = (
    req: express.Request,
    res: express.Response
  ) => {
    const id = req.params.id;
    console.log(`Invoked: getFileFeaturesById with 
    id: ${id}
    `);
    File_featuresModel.findById(id).then((fileData) => {
      if (fileData) {
        res.send(fileData);
      } else {
        res.sendStatus(404);
      }
    });
  };
}

export default FileFeaturesController;
