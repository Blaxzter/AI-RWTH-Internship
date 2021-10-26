import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import FontAwesomeIcon from "@/utilities/fontawesome-icons";

createApp(App)
  .component("font-awesome-icon", FontAwesomeIcon)
  .use(store)
  .use(router)
  .mount("#app");
