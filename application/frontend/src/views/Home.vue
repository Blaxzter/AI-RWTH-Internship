<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
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
