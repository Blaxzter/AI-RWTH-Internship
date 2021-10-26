<template>
  <div class="navigation">
    <ul class="nav flex-column">
      <li class="nav-item my-3">
        <router-link class="nav-link py-2" active-class="active" to="/">
          Home
        </router-link>
      </li>
      <li class="nav-item my-3">
        <router-link class="nav-link py-2" active-class="active" to="/about">
          About
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "navigation",
  props: {
    menuCollapsed: Boolean, // previously was `value: String`
  },
});
</script>

<style lang="scss">
.active {
  font-weight: bold;
  background-color: #f1f2f3;
  box-shadow: inset -5px 0px 0px 0px rgba(231, 166, 26, 1);
}
</style>
