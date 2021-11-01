import express from "express";
import * as bodyParser from "body-parser";
import cors from "cors";
import "dotenv/config";

import FileServerController from "./controller/file-server.controller";
import Controller from "./interfaces/controller.interface";

import { connect, connection } from "mongoose";
import BackupMetadataController from "./controller/backup-metadata.controller";
import FileFeaturesController from "./controller/file-features.controller";

// noinspection JSUnusedLocalSymbols
const { MONGO_USER, MONGO_PASSWORD, MONGO_PATH } = process.env;

const app = express();
const port = 8081; // default port to listen

run().catch((err) => console.log(err));

async function run(): Promise<void> {
  console.log(`mongodb://${MONGO_PATH}`);
  await connect(`mongodb://${MONGO_PATH}`);
}

let foundCollection: String[] = [];

// On db connect
connection.on("open", function () {
  console.log("Connected to mongo server.");
  //trying to get collection names
  connection.db.listCollections().toArray(function (err, collection) {
    foundCollection = collection.map((c) => c.name);
    console.log(`Found following collections: ${foundCollection}`);
  });
});

// Parse the response to json
app.use(bodyParser.json());
app.use(cors());

// For each model we have create a middle ware
const modelController = [
  new FileServerController(),
  new BackupMetadataController(),
  new FileFeaturesController(),
];
modelController.forEach((controller: Controller) => {
  app.use("/", controller.router);
});

// Default route
app.get("/", (req, res) => {
  res.send({
    collections: foundCollection,
  });
});

// start the Express server
app.listen(port, () => {
  console.log(`server started at http://localhost:${port}`);
});
