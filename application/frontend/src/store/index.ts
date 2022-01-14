import { createStore } from "vuex";
import {
  IBackupMetadata,
  IFileFeatures,
  IFileServer,
} from "@/store/Interfaces";
import { fetchBackupMetadataByFileServer, fetchFileServers } from "@/store/api";

export interface State {
  fileServers: Array<IFileServer>;
  backupMetadata: Array<IBackupMetadata>;
  fileData: Array<IFileFeatures>;
}

export default createStore({
  state: {
    fileServers: Array<IFileServer>(),
    backupMetadata: Array<IBackupMetadata>(),
    fileData: Array<IFileFeatures>(),
  },
  mutations: {
    setFileServers(state, fileServers: Array<IFileServer>) {
      state.fileServers = fileServers;
    },
    addFileServer(state, fileServer: IFileServer) {
      state.fileServers.push(fileServer);
    },
    addBackupMetadata(state, backupMetadata: Array<IBackupMetadata>) {
      state.backupMetadata.push(...backupMetadata);
    },
  },
  getters: {
    getFileServers: ({ fileServers }) => {
      return fileServers;
    },
    getFileServer:
      ({ fileServers }) =>
      (id: string) => {
        return fileServers.find((fileServer) => fileServer._id == id);
      },
    getBackupMetadata:
      ({ backupMetadata }) =>
      (id: string) => {
        const filter = backupMetadata.filter(
          (backupMetadata) => backupMetadata.file_server_id == id
        );
        if (filter.length == 0) return null;
        return filter;
      },
  },
  actions: {
    getFileServers({ commit }) {
      return fetchFileServers().then((fileServers) => {
        commit("setFileServers", fileServers);
      });
    },
    getBackupMetadata({ commit }, { fileServerId }) {
      console.log("test");
      return fetchBackupMetadataByFileServer(fileServerId).then(
        (backupMetadata) => {
          commit("addBackupMetadata", backupMetadata);
        }
      );
    },
  },
  modules: {},
});
