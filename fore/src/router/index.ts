import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import HelloWorld from "@/views/HelloWorld.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Hello",
    component: HelloWorld
  },
  {
    path: "/storage",
    name: "Storage",
    component: () => import("@/views/StorageTable.vue")
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

export default router;
