import { generateError, generateSuccess } from "@/utils/result";
const STORAGE = window.sessionStorage;
const VueSession = {
  key: "vue-session-key",
  flash_key: "vue-session-flash-key",
  setAll: function(all) {
    STORAGE.setItem(VueSession.key, JSON.stringify(all));
  }
};
const instance = {
  flash: {
    get: function(key) {
      const all = instance.getAll();
      const all_flash = all[VueSession.flash_key] || {};
      const flash_value = all_flash[key];
      this.remove(key);
      return flash_value;
    },
    set: function(key, value) {
      const all = instance.getAll();
      const all_flash = all[VueSession.flash_key] || {};
      all_flash[key] = value;
      all[VueSession.flash_key] = all_flash;
      VueSession.setAll(all);
      return generateSuccess();
    },
    remove: function(key) {
      const all = instance.getAll();
      const all_flash = all[VueSession.flash_key] || {};
      delete all_flash[key];
      all[VueSession.flash_key] = all_flash;
      VueSession.setAll(all);
    }
  },
  getAll: function() {
    const all = JSON.parse(STORAGE.getItem(VueSession.key));
    return all || {};
  },
  set: function(key, value) {
    if (key == "session-id") return generateError();
    let all = this.getAll();
    if (!("session-id" in all)) {
      this.start();
      all = this.getAll();
    }
    all[key] = value;
    VueSession.setAll(all);
    return generateSuccess();
  },
  get: function(key) {
    const all = this.getAll();
    return all[key];
  },
  start: function() {
    const all = this.getAll();
    all["session-id"] = "sess:" + Date.now();
    VueSession.setAll(all);
  },
  renew: function(sessionId) {
    const all = this.getAll();
    all["session-id"] = "sess:" + sessionId;
    VueSession.setAll(all);
  },
  exists: function() {
    const all = this.getAll();
    return "session-id" in all;
  },
  has: function(key) {
    const all = this.getAll();
    return key in all;
  },
  remove: function(key) {
    const all = this.getAll();
    delete all[key];
    VueSession.setAll(all);
  },
  clear: function() {
    const all = this.getAll();
    VueSession.setAll({ "session-id": all["session-id"] });
  },
  destroy: function() {
    VueSession.setAll({});
  },
  id: function() {
    return this.get("session-id");
  }
};
export function getSessionInstance() {
  return instance;
}
export default instance;
//# sourceMappingURL=session.js.map
