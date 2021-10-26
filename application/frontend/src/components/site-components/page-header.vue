<template>
  <header class="header">
    <div class="container-xxl px-3 py-2 navbar justify-content-between">
      <div class="fs-2">FAbraham ML-Tool</div>
      <div class="d-flex">
        <div class="border p-2 d-flex align-items-baseline me-2">
          <font-awesome-icon class="me-2" icon="user" />
          <span>User</span>
        </div>
        <div class="border p-2 me-2">File Server</div>
        <div class="border p-2 me-2">Settings</div>
      </div>
    </div>
  </header>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "page-header",
});
</script>

<style lang="scss">
.header {
  box-shadow: 0 0.5rem 1rem rgb(0 0 0 / 5%), inset 0 -1px 0 rgb(0 0 0 / 15%);
}
</style>
