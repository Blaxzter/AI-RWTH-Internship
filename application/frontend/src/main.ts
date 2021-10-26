import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import FontAwesomeIcon from "@/utilities/fontawesome-icons";
import VueSidebarMenu from "vue-sidebar-menu";
import "vue-sidebar-menu/dist/vue-sidebar-menu.css";

createApp(App)
  .component("font-awesome-icon", FontAwesomeIcon)
  .use(VueSidebarMenu)
  .use(store)
  .use(router)
  .mount("#app");
