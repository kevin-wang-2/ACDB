<template>
  <el-main>
    <el-input
      v-model="search"
      suffix-icon="el-icon-search"
      ref="search"
    ></el-input>
  </el-main>
</template>

<script lang="ts">
import Vue from "vue";
import {} from "vue-router";
import Component from "vue-class-component";

@Component({
  beforeRouteEnter(to, from, next) {
    next(vm => {
      (vm as Search).search = vm.$route.params.search;
      vm.$nextTick(() => (vm.$refs.search as any).getInput().focus());
    });
  },
  beforeRouteLeave(to, from, next) {
    (this as Search).$emit("searchEnd", (this as Search).search);
    next();
  }
})
export default class Search extends Vue {
  name = "Search";
  search: string;
  constructor() {
    super();
    this.search = "";
  }
}
</script>

<style scoped></style>
