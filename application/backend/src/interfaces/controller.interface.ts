// Source
// https://wanago.io/2018/12/10/express-mongodb-typescript-env-var/

import { Router } from "express";

interface Controller {
  path: string;
  router: Router;
}

export default Controller;
