<template>
  <div>
    <div
      class="card"
      style="width: 18rem"
      v-for="fileServer in fileServers"
      :key="fileServer._id"
      @click="$router.push(`/file-server/${fileServer._id}`)"
    >
      <div class="card-body">
        <div
          class="
            card-title
            d-flex
            justify-content-between
            align-items-baseline
            mb-4
          "
        >
          <h5>File Server</h5>
          <font-awesome-icon class="me-2" icon="server" />
        </div>
        <h6 class="card-subtitle mb-2 text-muted text-start">
          Name: {{ fileServer.name }}
        </h6>
        <div class="card-text text-start">
          <div>Connection: {{ fileServer.con }}</div>
          <div>Check Schedule: {{ fileServer.check_schedule }}</div>
        </div>
        <div class="text-end hand-icon">
          <font-awesome-icon class="me-2" icon="hand-pointer" />
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
  data() {
    return {};
  },
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

<style lang="scss">
.card {
  &:hover {
    border-color: #2c3e50;
    cursor: pointer;

    .card-body .hand-icon {
      color: #2a5c90;
    }
  }
}
</style>
