<template>
  <div class="d-flex flex-column vh-100">
    <page-header />
    <div class="d-flex container-xxl pt-4 flex-grow-1">
      <navigation class="navigation" />
      <main class="container">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Navigation from "@/components/site-components/navigation.vue";
import PageHeader from "@/components/site-components/page-header.vue";

export default defineComponent({
  components: { PageHeader, Navigation },

  data: () => {
    return {
      menuCollapsed: false,
    };
  },
});
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
