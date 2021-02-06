import { Dict } from "@/types/utils";

interface TagConfig {
  category_name: Dict<string>;
  property_name: Dict<string>;
}

interface ModelConfig {
  server: string;
  tag: TagConfig;
}

interface Navigator {
  [key: string]: string;
}

interface Leveler {
  [key: string]: number;
}

export interface Config {
  navigator: Navigator;
  level: Leveler;
  model: ModelConfig;
}

export const config: Config = {
  model: {
    server: "http://127.0.0.1:5000",
    tag: {
      category_name: {
        "0": "属性",
        "1": "长度",
        "2": "接口",
        "3": "数量"
      },
      property_name: {
        length: "长度",
        socket: "接口",
        amount: "数量"
      }
    }
  },
  navigator: {
    "/": "1",
    "/storage": "2",
    "/stock": "3-2",
    "/tag": "3-3",
    "/contact": "3-4",
    "/search": "4"
  },
  level: {
    "*": 0,
    Index: -1,
    Storage: -1,
    Stock: 0,
    Tag: 0,
    Contact: 0,
    Search: 0
  }
};

export default config;
