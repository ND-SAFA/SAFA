import { defineStore } from "pinia";

import { pinia } from "@/plugins";
import { useApi } from "@/hooks";

export const useMemberApi = defineStore("useMemberApi", () => {
  const useMemberApi = useApi("useMemberApi");
});

export default useMemberApi(pinia);
