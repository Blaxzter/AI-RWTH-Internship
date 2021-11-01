//https://wanago.io/2018/12/10/express-mongodb-typescript-env-var/

import express from "express";
import Controller from "../interfaces/controller.interface";
import { FileServerModel, IFileServer } from "../models/file-server.model";

class FileServerController implements Controller {
  public path = "/file-servers";
  public router = express.Router();

  constructor() {
    this.initializeRoutes();
  }

  private initializeRoutes() {
    this.router.get(this.path, this.getAllFileServers);
    this.router.get(`${this.path}/:id`, this.getFileServerById);
    this.router.patch(`${this.path}/:id`, this.modifyFileServer);
    this.router.delete(`${this.path}/:id`, this.deleteFileServer);
    this.router.post(this.path, this.createFileServer);
  }

  private getAllFileServers = (req: express.Request, res: express.Response) => {
    console.log(`Invoked: getAllFileServers`);
    FileServerModel.find(req.query).then((file_server) => {
      res.send(file_server);
    });
  };

  private getFileServerById = (req: express.Request, res: express.Response) => {
    const id = req.params.id;
    console.log(`Invoked: getFileServerById with 
    id: ${id}
    `);
    FileServerModel.findById(id).then((fileServer) => {
      if (fileServer) {
        res.send(fileServer);
      } else {
        res.sendStatus(404);
      }
    });
  };

  private modifyFileServer = (req: express.Request, res: express.Response) => {
    const id = req.params.id;
    const fileServerData: IFileServer = req.body;
    console.log(
      `Invoked: modifyFileServer with 
      id ${id} 
      data ${JSON.stringify(fileServerData)}`
    );
    FileServerModel.findByIdAndUpdate(id, fileServerData, { new: true }).then(
      (post) => {
        res.send(post);
      }
    );
  };

  private createFileServer = (req: express.Request, res: express.Response) => {
    const fileServerData: IFileServer = req.body;
    console.log(
      `Invoked: createFileServer with 
      data ${JSON.stringify(fileServerData)}`
    );
    const createdFileServer = new FileServerModel(fileServerData);
    createdFileServer.save().then((savedFileServer) => {
      res.send(savedFileServer);
    });
  };

  private deleteFileServer = (req: express.Request, res: express.Response) => {
    const id = req.params.id;
    console.log(`Invoked: deleteFileServer with \n\tid: ${id}`);
    FileServerModel.findByIdAndDelete(id).then((successResponse) => {
      if (successResponse) {
        res.sendStatus(200);
      } else {
        res.sendStatus(404);
      }
    });
  };
}

export default FileServerController;
