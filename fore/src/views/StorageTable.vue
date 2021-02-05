<template>
  <el-main>
    <el-table
      :data="storage"
      stripe
      ref="table"
      @selection-change="handleSelectionChange"
      max-height="750"
      v-loading="loading"
    >
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column prop="name" label="名称" width="100"></el-table-column>
      <el-table-column prop="slots" label="标签">
        <template slot-scope="scope">
          <div v-for="tags in scope.row.slots" :key="JSON.stringify(tags)">
            <el-tag v-for="tag in tags" v-bind:key="tag" type="primary">
              {{ tag }}
            </el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="rent" label="可出租" width="100">
        <template slot-scope="scope">
          {{ scope.row.rent ? "可出租" : "不可出租" }}</template
        >
      </el-table-column>
    </el-table>
    <div style="margin-top: 20px">
      <el-button>租借</el-button>
    </div>
  </el-main>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import {} from "element-ui";
import { ElTable } from "element-ui/types/table";
import { StockModel, forEachSlots } from "@/types/model";
import axios from "axios";

@Component({
  beforeRouteEnter(from, to, next) {
    next(vm => {
      const app = vm as StorageTable;
      app.loading = true;
      axios.get("/api/stock").then(async result => {
        if (result.data.success) {
          const storage: StockModel[] = result.data.data;
          for (let i = 0; i < storage.length; i++)
            await forEachSlots(storage[i], async (item: string) => {
              const tag = await axios.get("/api/tag/" + item);
              return tag.data.data.name;
            });
          app.storage = storage;
          app.loading = false;
        } else {
          app.$message.error("加载失败");
        }
      });
    });
  }
})
export default class StorageTable extends Vue {
  name = "StorageTable";
  loading: boolean;
  storage: StockModel[];
  selectedItems: Array<StockModel> = [];
  constructor() {
    super();
    this.storage = [];
    this.loading = true;
  }

  handleSelectionChange(val: StockModel[]) {
    this.selectedItems = [];
    val.forEach(item => {
      if (!item.rent) {
        (this.$refs.table as ElTable).toggleRowSelection(item);
      } else {
        this.selectedItems.push(item);
      }
    });
  }
}
</script>

<style scoped></style>
