import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import HelloWorld from "@/views/HelloWorld.vue";

import store from "@/store";
import config from "@/config/config";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Index",
    component: HelloWorld
  },
  {
    path: "/storage",
    name: "Storage",
    component: () => import("@/views/StorageTable.vue")
  },
  {
    path: "/stock",
    name: "Stock",
    component: () => import("@/views/Stock.vue")
  },
  {
    path: "/tag",
    name: "Tag",
    component: () => import("@/views/TagTable.vue")
  },
  {
    path: "/search",
    name: "Search",
    component: () => import("@/views/Search.vue")
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  if (config.level[to.name || "Index"] > store.state.login.level)
    next({ name: "Index" });
  else next();
});

export default router;
