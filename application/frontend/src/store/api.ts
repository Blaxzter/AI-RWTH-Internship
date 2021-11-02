import { IBackupMetadata, IFileServer } from "@/store/Interfaces";
import axios, { AxiosResponse } from "axios";

const server_url = "http://localhost:8081";

export function fetchFileServers(): Promise<Array<IFileServer>> {
  return axios
    .get(`${server_url}/file-servers`)
    .then((res: AxiosResponse<Array<IFileServer>>) => {
      return res.data;
    });
}

export function fetchBackupMetadata(): Promise<Array<IBackupMetadata>> {
  return axios
    .get(`${server_url}/backup-metadata`)
    .then((res: AxiosResponse<Array<IBackupMetadata>>) => {
      return res.data;
    });
}

export function fetchBackupMetadataByFileServer(
  file_server_id: string
): Promise<Array<IBackupMetadata>> {
  console.log(file_server_id);
  return axios
    .get(`${server_url}/backup-metadata`, {
      params: {
        file_server: file_server_id,
      },
    })
    .then((res: AxiosResponse<Array<IBackupMetadata>>) => {
      return res.data;
    });
}
