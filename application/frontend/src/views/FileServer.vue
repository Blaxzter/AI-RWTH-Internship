<template>
  <div v-if="fileServer">
    <h2>File Server: {{ fileServer.name }}</h2>
    <div class="file-server--data">
      <div>{{ fileServer._id }}</div>
      <div>{{ fileServer.con }}</div>
      <div>{{ fileServer.check_schedule }}</div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { IFileServer } from "@/store/Interfaces";

export default defineComponent({
  name: "FileServer",
  computed: {
    fileServer(): IFileServer {
      return this.$store.getters.getFileServer(this.$route.params.id);
    },
  },
  beforeMount() {
    if (this.fileServer) {
      this.fetchFileServers();
    }
  },
  methods: {
    fetchFileServers() {
      // return the Promise from the action
      return this.$store.dispatch("getFileServers");
    },
  },
});
</script>

<style scoped></style>
