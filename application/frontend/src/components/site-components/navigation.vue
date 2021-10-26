<template>
  <sidebar-menu
    :menu="menu"
    :relative="true"
    :theme="'white-theme'"
    :collapsed="collapsed"
  />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { SidebarMenu } from "vue-sidebar-menu";
import { useWindowSize } from "vue-window-size";

export default defineComponent({
  name: "navigation",
  props: {
    menuCollapsed: Boolean, // previously was `value: String`
  },
  setup() {
    const { width, height } = useWindowSize();
    return {
      windowWidth: width,
      windowHeight: height,
    };
  },
  data() {
    return {
      menu: [
        {
          header: "Main Navigation",
          hiddenOnCollapse: true,
        },
        {
          href: "/",
          title: "Dashboard",
          icon: {
            element: "font-awesome-icon",
            attributes: { icon: "home" },
          },
        },
        {
          href: "/about",
          title: "About",
          icon: {
            element: "font-awesome-icon",
            attributes: { icon: "user" },
          },
          child: [
            {
              href: "/charts/sublink",
              title: "Sub Link",
            },
          ],
        },
      ],
    };
  },
  components: {
    SidebarMenu,
  },
  computed: {
    collapsed() {
      return this.windowWidth < 700;
    },
  },
});
</script>

<style lang="scss">
.vsm--link {
  .svg-inline--fa {
    padding: 4px;
  }
}

.active {
  font-weight: bold;
  background-color: #f1f2f3;
  box-shadow: inset -5px 0px 0px 0px rgba(231, 166, 26, 1);
}
</style>
