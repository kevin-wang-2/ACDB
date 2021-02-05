<template>
  <div id="app">
    <Login
      v-if="!this.$store.state.login.success && !this.$store.state.login.tour"
      class="dialog-login"
    ></Login>
    <el-container class="dialog-main" v-else>
      <el-header>
        <el-menu :default-active="'1'" mode="horizontal">
          <el-menu-item index="1" @click="triggerRoute('/')">仓储</el-menu-item>
          <el-menu-item index="2" @click="triggerRoute('storage')"
            >库存列表</el-menu-item
          >
          <el-submenu index="3">
            <template slot="title">管理工具</template>
            <el-menu-item
              index="3-1"
              @click="onLogout()"
              v-if="!this.$store.state.login.tour"
              >登出</el-menu-item
            >
            <el-menu-item index="3-1" @click="triggerLogin()" v-else
              >登录</el-menu-item
            >
            <el-menu-item index="3-2" @click="triggerRoute('stock')"
              >进货</el-menu-item
            >
            <el-menu-item index="3-3" @click="triggerRoute('tag')"
              >标签编辑</el-menu-item
            >
            <el-menu-item index="3-3" @click="triggerRoute('contact')"
              >AC通讯录</el-menu-item
            >
          </el-submenu>
          <el-menu-item
            index="4"
            @click="triggerSearch()"
            v-if="this.$route.path !== '/search'"
          >
            <el-input v-model="search" suffix-icon="el-icon-search"></el-input>
          </el-menu-item>
        </el-menu>
      </el-header>
      <router-view
        @searchEnd="search => searchEndTriggered(search)"
      ></router-view>
      <el-footer class="footer" height="2rem">
        Developed by SJTU Art Center
      </el-footer>
    </el-container>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import {} from "vuex";
import {} from "element-ui";
import {} from "vue-router";
import Component from "vue-class-component";

import Login from "@/components/Login.vue";

@Component({
  components: {
    Login
  }
})
export default class App extends Vue {
  name = "app";
  search: string;
  searchTriggered: boolean;
  constructor() {
    super();
    this.search = "";
    this.searchTriggered = false;
  }
  async onLogout() {
    await this.$store.dispatch("logout");
  }
  triggerRoute(url: string) {
    this.searchTriggered = false;
    this.$router.push(url);
  }
  triggerLogin() {
    this.$store.commit("setTouristMode", false);
  }
  triggerSearch() {
    this.searchTriggered = true;
    this.$router.push({
      name: "Search",
      params: {
        search: this.search
      }
    });
  }
  searchEndTriggered(search: string) {
    this.search = search;
  }
}
</script>

<style scoped>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  padding-top: 60px;
  margin-top: 0;
  height: calc(100% - 60px);
  width: 100%;
  top: 0;
  left: 0;
  position: absolute;
}

.dialog-main {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
}

.main {
}

.footer {
  color: #777;
  margin-top: 0.5rem;
}
</style>
