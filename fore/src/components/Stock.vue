<template>
  <div>
    <el-form v-model="form">
      <el-form-item prop="name" label="名称">
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
          :titles="['可选标签', '插槽' + curSlot]"
        >
        </el-transfer>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: "Stock",
  data() {
    this.$axios.get("/api/tag").then(result => {
      const data = result.data.data;
      data.forEach(item =>
        this.tags.push({
          key: item._id,
          label: item.name
        })
      );
      this.loading = false;
    });

    return {
      form: {
        name: "",
        slots: [[]]
      },
      slotCnt: 1,
      curSlot: 0,
      tags: []
    };
  },
  methods: {
    async onSubmit() {
      this.$axios.post("/api/stock", this.$qs.stringify(this.form));
    }
  }
};
</script>

<style scoped>
.pos_left {
  text-align: left;
}

.separator {
  margin-left: 1rem;
  margin-right: 1rem;
}
</style>
