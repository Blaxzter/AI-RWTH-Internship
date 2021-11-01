import { IFileServer } from "@/store/Interfaces";
import axios, { AxiosResponse } from "axios";

const server_url = "http://localhost:8081";

export function fetchFileServers() {
  return axios
    .get(`${server_url}/file-servers`)
    .then((res: AxiosResponse<IFileServer>) => {
      return res.data;
    });
}
