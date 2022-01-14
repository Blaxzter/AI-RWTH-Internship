<template>
  <div class="home text-start">
    <h1 class="mb-5">File Servers:</h1>
    <file-server-list />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import FileServerList from "@/components/home-components/FileServerList.vue";

export default defineComponent({
  name: "Home",
  components: { FileServerList },
  computed: {
    fileServers() {
      return this.$store.state.fileServers;
    },
  },
});
</script>
