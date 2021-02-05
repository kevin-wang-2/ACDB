import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./plugins/element.js";

Vue.config.productionTip = false;

// 配置config
import axios from "axios";
import qs from "qs";
import config from "@/config/config";

axios.defaults.baseURL = config.model.server;

const app = new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");

app.$config = config;
app.$axios = axios;
app.$qs = qs;

app.$store.dispatch("renew");
setInterval(() => {
  if (app.$store.state.login.success && !app.$store.state.login.tour)
    app.$store.dispatch("renew");
}, 10000);
