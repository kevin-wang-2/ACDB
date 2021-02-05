import config from "@/config/config";
import axios from "axios";
import qs from "qs";

declare module "vue/types/vue" {
  interface Vue {
    $config?: typeof config;
    $axios?: typeof axios;
    $qs?: typeof qs;
  }
}
