<template>
  <div>
    <el-table :data="tags" max-height="750" v-loading="loading">
      <el-table-column prop="name" label="名称" width="100"></el-table-column>
      <el-table-column
        prop="category"
        label="类型"
        width="100"
        :filters="
          (() => {
            let filter = [];
            for (let key in category_name) {
              if (!category_name.hasOwnProperty(key)) continue;
              filter.push({ text: category_name[key], value: parseInt(key) });
            }
            return filter;
          })()
        "
        :filter-method="filterHandler"
      >
        <template slot-scope="scope">
          {{ uconfig.model.tag.category_name[scope.row.category] }}
        </template>
      </el-table-column>
      <el-table-column prop="property" label="属性">
        <template slot-scope="scope">
          <el-tag v-for="(property, key) in scope.row.property" :key="key">
            {{ uconfig.model.tag.property_name[key] }}: {{ property }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-popconfirm
            title="删除这一个标签?"
            @confirm="deleteTag(scope.row._id)"
          >
            <el-button type="text" size="medium" slot="reference"
              >删除</el-button
            >
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <div style="margin-top: 20px">
      <el-popover placement="bottom" v-model="visible">
        <el-form
          ref="form"
          :model="form"
          label-width="4rem"
          @keyup.enter.native="onSubmit"
          @submit.native.prevent
          :rules="{
            tag_name: [{ required: true, message: '标签名不能为空' }],
            tag_category: [{ required: true, message: '请选择一种标签类型' }]
          }"
        >
          <el-form-item label="标签" prop="tag_name">
            <el-input v-model="form.name" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="类型" prop="tag_category">
            <el-select v-model="form.category" @change="changeCategory">
              <el-option
                v-for="(name, key) in category_name"
                :key="key"
                :value="key"
                :label="name"
              >
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item
            v-for="element in tag_property_input"
            :key="element.key"
            :label="element.label"
            :rules="element.rules"
            :prop="'property.' + element.key"
          >
            <component
              :is="element.type"
              v-model="form.property[element.key]"
              filterable
            >
              <component
                v-for="option in element.options"
                :key="option.key"
                :value="option.value"
                :is="option.type || 'el-option'"
                :label="option.label || option.key"
              >
              </component>
            </component>
          </el-form-item>
          <el-form-item>
            <el-button @click="onSubmit">添加</el-button>
          </el-form-item>
        </el-form>
        <el-button type="primary" slot="reference">添加标签</el-button>
      </el-popover>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import {} from "element-ui";
import { TagModel, SubmitTagModel, PropertyType } from "@/types/tag";

import config from "@/config/config";
import axios from "axios";
import qs from "qs";
import { FormValidatorGroup, Option } from "@/types/form";

interface PropertyInputField {
  key: string;
  type: string;
  label: string;
  rules: FormValidatorGroup;
  options?: Option[];
}

type PropertyInputFieldGroup = PropertyInputField[];

interface PropertyInputFieldTree {
  [key: string]: PropertyInputFieldGroup;
}

const property_input_fields: PropertyInputFieldTree = {
  "0": [],
  "1": [
    {
      key: "length",
      type: "el-input",
      label: "长度",
      rules: [
        { required: true, message: "长度数值不能为空" },
        {
          validator(rule, value: string, cb) {
            if (value === "") cb(new Error("长度数值不能为空"));
            else if (isNaN(parseFloat(value))) cb(new Error("长度必须是数值"));
            else cb();
          }
        }
      ]
    }
  ],
  "2": [
    {
      key: "socket",
      type: "el-select",
      label: "接口",
      rules: [{ required: true, message: "长度数值不能为空" }],
      options: [
        { key: "XLR (M)", value: 0 },
        { key: "XLR (F)", value: 1 },
        { key: "6.5TS", value: 2 },
        { key: "6.5TRS", value: 3 },
        { key: "3.5", value: 4 },
        { key: "3.5 (F)", value: 5 },
        { key: "RCA", value: 6 },
        { key: "MIDI", value: 7 },
        { key: "VGA", value: 8 },
        { key: "HDMI", value: 9 },
        { key: "NET", value: 10, label: "网线" }
      ]
    }
  ]
};

@Component({
  beforeRouteEnter(from, to, next) {
    next(vm => {
      const app: TagTable = vm as TagTable;
      axios.get("/api/tag").then(result => {
        if (result.data.success) {
          app.tags = result.data.data;
          app.loading = false;
        } else {
          app.$message.error("加载失败");
        }
      });
    });
  }
})
export default class TagTable extends Vue {
  name = "TagTable";
  tags: Array<TagModel<PropertyType>>;
  loading: boolean;
  visible: boolean;
  form: TagModel<PropertyType>;
  tag_property_input: PropertyInputFieldGroup;
  category_name = config.model.tag.category_name;
  uconfig = config;

  constructor() {
    super();
    this.tags = [];
    this.loading = true;
    this.visible = false;
    this.form = {
      name: "",
      category: "",
      property: {}
    };
    this.tag_property_input = property_input_fields["0"];
  }
  async onSubmit() {
    console.log(this.form);
    const tag: SubmitTagModel = {
      name: this.form.name,
      category: this.form.category
    };
    for (const key in this.form.property) {
      (tag as any)[key] = (this.form.property as any)[key];
    }

    const result = await axios.post("/api/tag", qs.stringify(tag));
    if (result.data.success) {
      this.$message({
        message: "创建成功",
        type: "success"
      });
    } else {
      this.$message.error("创建失败");
    }

    this.loading = true;
    axios.get("/api/tag").then(result => {
      this.tags = result.data.data;
      this.loading = false;
    });
  }

  changeCategory() {
    this.form.property = {};
    this.tag_property_input = property_input_fields[this.form.category];
  }

  filterHandler(value: string, row: TagModel<PropertyType>) {
    const category = row["category"];
    return category === value;
  }

  deleteTag(id: string) {
    axios
      .delete("/api/tag?" + qs.stringify({ id }))
      .then(result => {
        if (result.data.success) {
          this.$message({
            message: "删除成功",
            type: "success"
          });
        } else {
          this.$message.error("删除失败");
        }

        this.loading = true;
        return axios.get("/api/tag");
      })
      .then(result => {
        this.tags = result.data.data;
        this.loading = false;
      });
  }
}
</script>

<style scoped></style>
