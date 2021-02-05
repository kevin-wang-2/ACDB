import { Store, MutationTree, ActionContext } from "vuex";

export interface LoginData {
  success: boolean;
  sid: string;
  level: number;
  token: "";
}

export interface LoginDataWithTourMode extends LoginData {
  tour: boolean;
}

export interface LoginDataBase {
  login: LoginDataWithTourMode;
}

export function generateLoginState(): LoginDataWithTourMode {
  return {
    success: false,
    sid: "",
    level: -1,
    token: "",
    tour: false
  };
}

type LoginMutationType = MutationTree<LoginDataBase>;

export const loginMutations: LoginMutationType = {
  setLogin(state: LoginDataBase, data: LoginData) {
    state.login.success = data.success;
    state.login.sid = data.sid;
    state.login.level = data.level;
    state.login.token = data.token;
    state.login.tour = false;
  },
  setTouristMode(state: LoginDataBase, mode?: boolean) {
    state.login.tour = mode || false;
  }
};

import axios from "axios";
import qs from "qs";
import session from "@/store/session";
import { Result, generateSuccess, generateError } from "@/utils/result";

export interface LoginForm {
  username: string;
  password: string;
}

export const loginActions = {
  login(
    this: Store<LoginDataBase>,
    context: ActionContext<LoginDataBase, LoginDataBase>,
    form: LoginForm
  ): Promise<Result<null>> {
    return axios
      .post("/api/login", qs.stringify(form), { withCredentials: true })
      .then(result => {
        if (result.data.success) {
          context.commit("setLogin", {
            success: true,
            sid: form.username,
            level: result.data.level,
            token: result.data.token
          });
          session.set<string>("token", result.data.token);
          context.commit("setTouristMode", false);
          axios.defaults.headers.authentication = result.data.token;
          return generateSuccess(null);
        } else {
          context.commit("setLogin", {
            success: false,
            sid: "",
            level: -1,
            token: ""
          });
          session.set<string>("token", "");
          context.commit("setTouristMode", false);
          axios.defaults.headers.authentication = result.data.token;
          return generateError(result.data.error);
        }
      });
  },
  logout(
    this: Store<LoginDataBase>,
    context: ActionContext<LoginDataBase, LoginDataBase>
  ): Promise<Result<null>> {
    return axios.get("/api/logout", { withCredentials: true }).then(result => {
      context.commit("setLogin", {
        success: false,
        sid: "",
        level: -1,
        token: ""
      });
      session.set<string>("token", "");
      context.commit("setTouristMode", false);
      axios.defaults.headers.authentication = "";
      if (result.data.success) {
        return generateSuccess(null);
      } else {
        return generateError(result.data.error);
      }
    });
  },
  renew(
    this: Store<LoginDataBase>,
    context: ActionContext<LoginDataBase, LoginDataBase>
  ): Promise<Result<null>> {
    // 未登录并没有session记录
    if (this.state.login.token === "" && !session.get("token"))
      return new Promise(res => res(generateError(-1)));
    const token = this.state.login.token || session.get("token");
    return axios
      .get("/api/refresh", {
        headers: { authentication: token },
        withCredentials: true
      })
      .then(result => {
        if (result.data.success) {
          context.commit("setLogin", {
            success: true,
            sid: result.data.sid,
            level: result.data.level,
            token: result.data.token
          });
          session.set<string>("token", result.data.token);
          context.commit("setTouristMode", false);
          axios.defaults.headers.authentication = result.data.token;
          return generateSuccess(null);
        } else {
          context.commit("setLogin", {
            success: false,
            sid: "",
            level: -1,
            token: ""
          });
          session.set<string>("token", "");
          context.commit("setTouristMode", false);
          axios.defaults.headers.authentication = "";
          return generateError(result.data.error);
        }
      });
  }
};
