//https://wanago.io/2018/12/10/express-mongodb-typescript-env-var/

import express from "express";
import Controller from "../interfaces/controller.interface";
import {
  BackupMetadataModel,
  IBackupMetadata,
} from "../models/backup-metadata.model";

class BackupMetadataController implements Controller {
  public path = "/backup-metadata";
  public router = express.Router();

  constructor() {
    this.initializeRoutes();
  }

  private initializeRoutes() {
    this.router.get(this.path, this.getBackupMetadata);
    this.router.get(`${this.path}/:id`, this.getBackupMetadataById);
    this.router.delete(`${this.path}/:id`, this.deleteBackupMetadataById);
    this.router.post(this.path, this.createBackupMetadata);
  }

  private getBackupMetadata = (req: express.Request, res: express.Response) => {
    console.log(`Invoked: getBackupMetadata`);
    BackupMetadataModel.find(req.query).then((file_server) => {
      res.send(file_server);
    });
  };

  private getBackupMetadataById = (
    req: express.Request,
    res: express.Response
  ) => {
    const id = req.params.id;
    console.log(`Invoked: getBackupMetadataById with 
    id: ${id}
    `);
    BackupMetadataModel.findById(id).then((backupMetadata) => {
      if (backupMetadata) {
        res.send(backupMetadata);
      } else {
        res.sendStatus(404);
      }
    });
  };

  private createBackupMetadata = (
    req: express.Request,
    res: express.Response
  ) => {
    const fileServerData: IBackupMetadata = req.body;
    console.log(
      `Invoked: createBackupMetadata with 
      data ${JSON.stringify(fileServerData)}`
    );
    const createdFileServer = new BackupMetadataModel(fileServerData);
    createdFileServer.save().then((savedFileServer) => {
      res.send(savedFileServer);
    });
  };

  private deleteBackupMetadataById = (
    req: express.Request,
    res: express.Response
  ) => {
    const id = req.params.id;
    console.log(`Invoked: deleteBackupMetadataById with \n\tid: ${id}`);
    BackupMetadataModel.findByIdAndDelete(id).then((successResponse) => {
      if (successResponse) {
        res.sendStatus(200);
      } else {
        res.sendStatus(404);
      }
    });
  };
}

export default BackupMetadataController;
