<template>
  <div class="shader">
    <div class="login-container">
      <el-container class="login">
        <el-header class="title">
          <h2>
            登录
          </h2>
        </el-header>
        <el-main>
          <el-form
            ref="form"
            :model="form"
            label-width="4rem"
            @keyup.enter.native="onLogin"
            @submit.native.prevent
            :rules="{
              username: [
                {
                  required: true,
                  message: '学号不能为空'
                }
              ],
              password: [
                {
                  required: true,
                  message: '密码不能为空'
                }
              ]
            }"
          >
            <el-form-item label="学号" prop="username">
              <el-input v-model="form.username" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input
                v-model="form.password"
                type="password"
                autocomplete="off"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onLogin">登录</el-button>
              <el-button>忘记密码</el-button>
              <el-button @click="tour">游客模式</el-button>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script lang="ts">
import { Result } from "@/utils/result";
import { Component, Vue } from "vue-property-decorator";
import { LoginForm } from "@/store/login";
import {} from "vuex";
import {} from "element-ui";

@Component({})
export default class Login extends Vue {
  name = "login";
  form: LoginForm;
  constructor() {
    super();
    this.form = {
      username: "",
      password: ""
    };
  }
  async onLogin() {
    const result: Result<null> = await this.$store.dispatch("login", this.form);
    if (result.success) {
      this.$message.success("登陆成功");
    } else {
      this.$message.error("登陆失败");
    }
  }
  tour() {
    this.$store.commit("setTouristMode", true);
  }
}
</script>

<style scoped>
.login {
  width: 30%;
  border: 1px solid #eee;
  border-radius: 5px;
  background-color: #fff;
}

.title {
  background-color: #ffffff;
}

.login-container {
  position: relative;
  left: 35%;
}

.shader {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: calc(100% - 60px);
  background-color: #f9f9f9;
  padding-top: 60px;
  z-index: 999;
}
</style>
