<template>
  <div>
    <div class="card" style="width: 18rem">
      <div
        class="card-body"
        v-for="fileServer in fileServers"
        :key="fileServer._id"
      >
        <h5 class="card-title">File Server</h5>
        <h6 class="card-subtitle mb-2 text-muted">
          Name: {{ fileServer.name }}
        </h6>
        <div class="card-text">
          <div>Connection: {{ fileServer.con }}</div>
          <div>Check Schedule: {{ fileServer.check_schedule }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { IFileServer } from "@/store/Interfaces";
import { defineComponent } from "vue";

export default defineComponent({
  name: "FileServerList",
  computed: {
    fileServers(): Array<IFileServer> {
      return this.$store.state.fileServers;
    },
  },
  mounted() {
    console.log(this.fileServers.length);
    if (this.fileServers.length === 0) {
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
