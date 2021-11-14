import { Store } from "vuex";
import { RootState } from "@/types/store/general";

declare module "@vue/runtime-core" {
  interface ComponentCustomProperties {
    $store: Store<RootState>;
  }
}
