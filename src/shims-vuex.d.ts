import { Store } from "vuex";
import { RootState } from "@/types/store";

declare module "@vue/runtime-core" {
  interface ComponentCustomProperties {
    $store: Store<RootState>;
  }
}
