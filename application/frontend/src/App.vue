<template>
  <div>
    <page-header v-model:menuCollapsed="menuCollapsed" />
    <div class="layout container-xxl pt-4">
      <navigation class="navigation" :class="{ mobile: menuCollapsed }" />
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
@import "~bootstrap/scss/_functions.scss";
@import "~bootstrap/scss/_variables.scss";
@import "~bootstrap/scss/_mixins.scss";

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.layout {
  display: grid;
  gap: 1.5rem;
  grid-template-areas: "sidebar main";
  grid-template-columns: 1fr 3fr;

  .navigation {
    grid-area: sidebar;
  }

  main {
    grid-area: main;
  }

  @include media-breakpoint-down(md) {
    grid-template-areas: "main";
    grid-template-columns: 4fr;
    gap: 0rem;

    .navigation {
      display: none;
    }

    .navigation.mobile {
      display: block;
      position: fixed;
    }
  }
}
</style>
