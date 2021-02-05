import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

import {
  generateLoginState,
  loginMutations,
  loginActions
} from "@/store/login";
import { curryMerge } from "@/utils/mergeObject";

export default new Vuex.Store({
  state: {
    login: generateLoginState()
  },
  mutations: curryMerge(loginMutations).value,
  actions: curryMerge(loginActions).value,
  modules: {}
});
