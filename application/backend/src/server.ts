import express from "express";
import * as bodyParser from "body-parser";
import "dotenv/config";
import FileServerController from "./models/file-server";
import Controller from "./interfaces/controller.interface";

import { connect, connection } from "mongoose";

// noinspection JSUnusedLocalSymbols
const { MONGO_USER, MONGO_PASSWORD, MONGO_PATH } = process.env;

const app = express();
const port = 8081; // default port to listen

run().catch((err) => console.log(err));

async function run(): Promise<void> {
  console.log(`mongodb://${MONGO_PATH}`);
  await connect(`mongodb://${MONGO_PATH}`);
}

// On db connect
connection.on("open", function () {
  console.log("Connected to mongo server.");
  //trying to get collection names
  connection.db.listCollections().toArray(function (err, collection) {
    console.log(
      `Found following collections: ${collection.map((c) => c.name)}`
    );
  });
});

// Parse the response to json
app.use(bodyParser.json());

// For each model we have create a middle ware
const modelController = [new FileServerController()];
modelController.forEach((controller: Controller) => {
  app.use("/", controller.router);
});

// start the Express server
app.listen(port, () => {
  console.log(`server started at http://localhost:${port}`);
});
