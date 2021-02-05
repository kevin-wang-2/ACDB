import { Result, generateError, generateSuccess } from "@/utils/result";

type SessionKey = string | number;
type SessionValue<T> = T;
type SessionGetter = <T>(key: SessionKey) => SessionValue<T>;
type SessionSetter = <T>(
  key: SessionKey,
  value: SessionValue<T>
) => Result<void>;
type SessionRemove = (key: SessionKey) => void;
type SessionRenew = (sessionId: string) => void;

interface SessionFlash {
  get: SessionGetter;
  set: SessionSetter;
  remove: SessionRemove;
}

export interface SessionTree {
  [key: string]: SessionValue<any>;
}

interface SessionStorage {
  flash: SessionFlash;
  getAll: () => SessionTree;
  set: SessionSetter;
  get: SessionGetter;
  start: () => void;
  renew: SessionRenew;
  exists: () => boolean;
  has: (key: SessionKey) => boolean;
  remove: (key: SessionKey) => void;
  clear: () => void;
  destroy: () => void;
  id: () => string;
}

const STORAGE = window.sessionStorage;
const VueSession = {
  key: "vue-session-key",
  flash_key: "vue-session-flash-key",
  setAll: function(all: SessionTree) {
    STORAGE.setItem(VueSession.key, JSON.stringify(all));
  }
};

const instance = {
  flash: {
    get: function(key: SessionKey) {
      const all = instance.getAll();
      const all_flash = all[VueSession.flash_key] || {};

      const flash_value = all_flash[key];

      this.remove(key);

      return flash_value;
    },
    set: function<T>(key: SessionKey, value: SessionValue<T>) {
      const all = instance.getAll();
      const all_flash = all[VueSession.flash_key] || {};

      all_flash[key] = value;
      all[VueSession.flash_key] = all_flash;

      VueSession.setAll(all);

      return generateSuccess<void>();
    },
    remove: function(key: SessionKey) {
      const all = instance.getAll();
      const all_flash = all[VueSession.flash_key] || {};

      delete all_flash[key];

      all[VueSession.flash_key] = all_flash;
      VueSession.setAll(all);
    }
  },
  getAll: function() {
    const all = JSON.parse(STORAGE.getItem(VueSession.key) as string);
    return all || {};
  },
  set: function<T>(key: SessionKey, value: SessionValue<T>): Result<void> {
    if (key == "session-id") return generateError<void>();
    let all = this.getAll();

    if (!("session-id" in all)) {
      this.start();
      all = this.getAll();
    }

    all[key] = value;

    VueSession.setAll(all);

    return generateSuccess<void>();
  },
  get: function(key: SessionKey) {
    const all = this.getAll();
    return all[key];
  },
  start: function() {
    const all = this.getAll();
    all["session-id"] = "sess:" + Date.now();

    VueSession.setAll(all);
  },
  renew: function(sessionId: string) {
    const all = this.getAll();
    all["session-id"] = "sess:" + sessionId;
    VueSession.setAll(all);
  },
  exists: function() {
    const all = this.getAll();
    return "session-id" in all;
  },
  has: function(key: SessionKey) {
    const all = this.getAll();
    return key in all;
  },
  remove: function(key: SessionKey) {
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

export function getSessionInstance(): SessionStorage {
  return instance;
}

export default instance;
