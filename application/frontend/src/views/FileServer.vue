<template>
  <div v-if="fileServer">
    <h2 class="text-start">File Server: {{ fileServer.name }}</h2>
    <div class="file-server--data text-start mb-5">
      <div>File Server ID: {{ fileServer._id }}</div>
      <div>File Server Connection: {{ fileServer.con }}</div>
      <div>Check Schedule: {{ fileServer.check_schedule }}</div>
    </div>
    <backup-list :file-server-id="fileServer._id" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import BackupList from "@/components/file-server-components/BackupList.vue";

export default defineComponent({
  name: "FileServer",
  components: { BackupList },
  computed: {
    fileServer() {
      return this.$store.getters.getFileServer(this.$route.params.id);
    },
  },
  beforeMount() {
    if (!this.fileServer) {
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
