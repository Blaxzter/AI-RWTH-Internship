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
  actions: {
    getFileServers({ commit }) {
      return fetchFileServers().then((fileServers) => {
        console.log(fileServers);
        commit("setFileServers", fileServers);
      });
    },
  },
  modules: {},
});
