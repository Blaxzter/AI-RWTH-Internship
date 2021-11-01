import { createStore } from "vuex";
import { IFileServer } from "@/store/Interfaces";
import { fetchFileServers } from "@/store/api";

export interface State {
  fileServers: Array<IFileServer>;
}

export default createStore({
  state: {
    fileServers: Array<IFileServer>(),
  },
  mutations: {
    setFileServers(state, fileServers: Array<IFileServer>) {
      state.fileServers = fileServers;
    },
    addFileServer(state, fileServer: IFileServer) {
      state.fileServers.push(fileServer);
    },
  },
  getters: {
    getFileServer:
      ({ fileServers }) =>
      (id: string) => {
        console.log(id);
        return fileServers.find((fileServer) => fileServer._id == id);
      },
  },
  actions: {
    getFileServers({ commit }) {
      return fetchFileServers().then((fileServers) => {
        commit("setFileServers", fileServers);
      });
    },
  },
  modules: {},
});
