<template>
  <el-main>
    <el-container>
      <el-aside width="40rem">
        <el-form v-model="form" :rules="validator">
          <el-form-item
            class="pos-left no-header"
            style="padding-right: 1rem"
            prop="name"
            label="名称"
          >
            <el-input v-model="form.name" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item class="pos-left" label="当前插槽">
            <el-input-number
              v-model="curSlot"
              :min="1"
              :max="slotCnt"
            ></el-input-number>
            <span class="separator">/</span>
            <el-input-number
              v-model="slotCnt"
              :min="1"
              @change="handleMaxChange()"
            ></el-input-number>
            <el-button @click="deleteCurSlot()" v-if="slotCnt > 1"
              >删除插槽</el-button
            >
          </el-form-item>
          <el-form-item class="pos-left" prop="slot">
            <el-transfer
              filterable
              v-model="form.slots[curSlot - 1]"
              :data="tags"
              :titles="['可选标签', '插槽' + curSlot.toString()]"
              v-loading="loading"
            >
            </el-transfer>
          </el-form-item>
          <el-form-item class="pos-left" label="可出借">
            <el-checkbox v-model="form.rent"></el-checkbox>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit">提交</el-button>
          </el-form-item>
        </el-form>
      </el-aside>
      <el-main class="no-header border-left">
        <el-collapse v-model="activeSlot">
          <el-collapse-item v-for="cnt in slotCnt" :key="cnt" :name="cnt">
            <template slot="title"> 插槽{{ cnt }} </template>
            <el-row v-for="(item, index) in form.slots[cnt - 1]" :key="item">
              <span style="min-width: 5rem;display: inline-block;">
                {{ tags.find(tag => tag.key === item).label }}
              </span>
              <el-button
                size="mini"
                @click="moveUpItem(cnt - 1, index)"
                v-if="index !== 0"
                icon="el-icon-arrow-up"
              ></el-button>
              <el-button
                size="mini"
                @click="moveDownItem(cnt - 1, index)"
                v-if="index !== form.slots[cnt - 1].length - 1"
                icon="el-icon-arrow-down"
              ></el-button>
            </el-row>
            <el-row v-if="slotCnt > 1" style="margin-top: 0.2rem">
              <el-button
                size="small"
                @click="moveUp(cnt - 1)"
                v-if="cnt !== 1"
                icon="el-icon-arrow-up"
                >上移</el-button
              >
              <el-button
                size="small"
                @click="moveDown(cnt - 1)"
                v-if="cnt !== slotCnt"
                icon="el-icon-arrow-down"
                >下移</el-button
              >
              <el-button size="small" @click="curSlot = cnt"
                >选择该插槽</el-button
              >
              <el-button size="small" @click="deleteSlot(cnt - 1)"
                >删除插槽</el-button
              >
            </el-row>
          </el-collapse-item>
        </el-collapse>
      </el-main>
    </el-container>
  </el-main>
</template>

<script lang="ts">
import Vue from "vue";
import {} from "element-ui";
import Component from "vue-class-component";

import axios from "axios";
import qs from "qs";
import { StockModel } from "@/types/model";
import { TagWithId } from "@/types/tag";
import { FormValidationTree, Option } from "@/types/form";

let slotCnt = 1;

@Component({
  beforeRouteEnter(from, to, next) {
    next(vm => {
      const app = vm as Stock;
      app.loading = true;
      app.loaded = true;
      axios.get("/api/tag").then(result => {
        app.tags = [];
        if (result.data.success) {
          result.data.data.forEach((item: TagWithId) => {
            app.tags.push({
              key: item._id,
              value: item._id,
              label: item.name
            });
          });
          app.loading = false;
        } else {
          app.$message.error("加载失败");
        }
      });
    });
  },
  mounted() {
    const app = this as Stock;
    if (!app.loaded) {
      app.loading = true;
      axios.get("/api/tag").then(result => {
        if (result.data.success) {
          app.tags = [];
          result.data.data.forEach((item: TagWithId) => {
            app.tags.push({
              key: item._id,
              value: item._id,
              label: item.name
            });
          });
          app.loading = false;
        } else {
          app.$message.error("加载失败");
        }
      });
      app.loaded = true;
    }
  }
})
export default class Stock extends Vue {
  name = "Stock";
  form: StockModel;
  slotCnt: number;
  curSlot: number;
  tags: Option[];
  loading: boolean;
  loaded: boolean;
  activeSlot: number[];
  validator: FormValidationTree = {
    name: [{ required: true, message: "名称不能为空" }],
    slot: [
      {
        validator: (rules, value, cb) => {
          for (let i = 0; i < slotCnt; i++) {
            if (this.form.slots[i].length === 0) {
              cb(new Error("不能有空插槽"));
              return;
            }
          }
          cb();
        }
      }
    ]
  };
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
    this.loaded = false;
    this.activeSlot = [1];
  }
  handleMaxChange() {
    // 保证一致性以免翻车
    if (this.form.slots.length > this.slotCnt) {
      this.form.slots = this.form.slots.slice(0, this.slotCnt);
    } else
      while (this.form.slots.length < this.slotCnt) {
        this.form.slots.push([]);
        this.activeSlot.push(this.form.slots.length);
      }
    if (this.curSlot > this.slotCnt) this.curSlot = this.slotCnt;
    this.activeSlot = this.activeSlot.filter(slot => slot <= this.slotCnt);
    slotCnt = this.slotCnt;
  }
  deleteCurSlot() {
    this.form.slots.splice(this.curSlot - 1, 1);
    this.slotCnt--;
    slotCnt--;
    if (this.curSlot > this.slotCnt) this.curSlot = this.slotCnt;
  }
  deleteSlot(slot: number) {
    this.form.slots.splice(slot, 1);
    this.slotCnt--;
    slotCnt--;
    if (this.curSlot > this.slotCnt) this.curSlot = this.slotCnt;
  }
  moveUpItem(slot: number, index: number) {
    const temp = this.form.slots[slot][index];
    this.form.slots[slot][index] = this.form.slots[slot][index - 1];
    this.form.slots[slot][index - 1] = temp;
    this.$forceUpdate();
  }
  moveDownItem(slot: number, index: number) {
    const temp = this.form.slots[slot][index];
    this.form.slots[slot][index] = this.form.slots[slot][index + 1];
    this.form.slots[slot][index + 1] = temp;
    this.$forceUpdate();
  }
  moveUp(slot: number) {
    const temp = this.form.slots[slot];
    this.form.slots[slot] = this.form.slots[slot - 1];
    this.form.slots[slot - 1] = temp;
    this.$forceUpdate();
  }
  moveDown(slot: number) {
    const temp = this.form.slots[slot];
    this.form.slots[slot] = this.form.slots[slot + 1];
    this.form.slots[slot + 1] = temp;
    this.$forceUpdate();
  }
  async onSubmit() {
    axios.post("/api/stock", qs.stringify(this.form)).then(result => {
      if (result.data.success) {
        this.form = {
          name: "",
          slots: [[]],
          rent: true
        };
        this.$message.success("进货成功");
      } else {
        if (result.data.error == -401) {
          this.$message.error("权限不足");
        } else {
          this.$message.error("添加失败");
        }
      }
    });
  }
}
</script>

<style scoped>
.no-header {
  margin-top: 0;
  padding-top: 0;
}

.label-header {
  padding-top: 12px;
}

.pos-left {
  text-align: left;
}

.border-left {
  border-left: 2px groove;
}

.separator {
  margin-left: 1rem;
  margin-right: 1rem;
}
</style>
