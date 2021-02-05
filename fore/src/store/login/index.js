export function generateLoginState() {
  return {
    success: false,
    sid: "",
    level: -1,
    token: "",
    tour: false
  };
}
export const loginMutations = {
  setLogin(state, data) {
    state.login.success = data.success;
    state.login.sid = data.sid;
    state.login.level = data.level;
    state.login.token = data.token;
    state.login.tour = false;
  },
  setTouristMode(state, mode) {
    state.login.tour = mode || false;
  }
};
import axios from "axios";
import qs from "qs";
import session from "@/store/session";
import { generateSuccess, generateError } from "@/utils/result";
export const loginActions = {
  login(context, form) {
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
          session.set("token", result.data.token);
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
          session.set("token", "");
          context.commit("setTouristMode", false);
          axios.defaults.headers.authentication = result.data.token;
          return generateError(result.data.error);
        }
      });
  },
  logout(context) {
    return axios.get("/api/logout", { withCredentials: true }).then(result => {
      if (result.data.success) {
        context.commit("setLogin", {
          success: false,
          sid: "",
          level: -1,
          token: ""
        });
        session.set("token", "");
        context.commit("setTouristMode", false);
        axios.defaults.headers.authentication = "";
        return generateSuccess(null);
      } else {
        return generateError(result.data.error);
      }
    });
  },
  renew(context) {
    // 未登录并没有session记录
    if (this.state.login.token === "" && !session.get("token"))
      return new Promise(res => res(generateError(-1)));
    const token = this.state.login.token || session.get("token");
    return axios
      .get("/api/refresh?token=" + token, { withCredentials: true })
      .then(result => {
        if (result.data.success) {
          context.commit("setLogin", {
            success: true,
            sid: result.data.sid,
            level: result.data.level,
            token: result.data.token
          });
          session.set("token", result.data.token);
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
          session.set("token", "");
          context.commit("setTouristMode", false);
          axios.defaults.headers.authentication = "";
          return generateError(result.data.error);
        }
      });
  }
};
//# sourceMappingURL=index.js.map
