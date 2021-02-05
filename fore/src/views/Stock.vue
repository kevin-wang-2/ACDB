<template>
  <div>
    <el-form v-model="form">
      <el-form-item prop="name" label="名称" class="pos_left">
        <el-input v-model="form.name" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item class="pos_left" label="当前插槽">
        <el-input-number
          v-model="curSlot"
          :min="0"
          :max="slotCnt - 1"
        ></el-input-number>
        <span class="separator">/</span>
        <el-input-number v-model="slotCnt" :min="0"></el-input-number>
      </el-form-item>
      <el-form-item class="pos_left">
        <el-transfer
          filterable
          v-model="form.slots[curSlot]"
          :data="tags"
          :titles="['可选标签', '插槽' + curSlot.toString()]"
          v-loading="loading"
        >
        </el-transfer>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import {} from "element-ui";
import Component from "vue-class-component";

import axios from "axios";
import qs from "qs";
import { StockModel } from "@/types/model";
import { TagWithId } from "@/types/tag";
import { Option } from "@/types/form";

@Component({
  beforeRouteEnter(from, to, next) {
    next(vm => {
      const app = vm as Stock;
      app.loading = true;
      axios.get("/api/tag").then(result => {
        if (result.data.success) {
          result.data.data.forEach((item: TagWithId) => {
            app.tags.push({
              key: item.name,
              value: item._id
            });
          });
          app.loading = false;
        } else {
          app.$message.error("加载失败");
        }
      });
    });
  }
})
export default class Stock extends Vue {
  name = "Stock";
  form: StockModel;
  slotCnt: number;
  curSlot: number;
  tags: Option[];
  loading: boolean;
  constructor() {
    super();
    this.form = {
      name: "",
      slots: [[]],
      rent: true
    };
    this.slotCnt = 1;
    this.curSlot = 0;
    this.tags = [];
    this.loading = true;
  }
  async onSubmit() {
    axios.post("/api/stock", qs.stringify(this.form));
  }
}
</script>

<style scoped>
.pos_left {
  text-align: left;
  margin-left: 2rem;
  margin-right: 2rem;
}

.separator {
  margin-left: 1rem;
  margin-right: 1rem;
}
</style>
