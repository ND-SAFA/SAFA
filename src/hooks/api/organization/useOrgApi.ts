import { defineStore } from "pinia";

import { useApi } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * A hook for managing requests to the organizations API.
 */
export const useOrgApi = defineStore("orgApi", () => {
  const orgApi = useApi("orgApi");
});

export default useOrgApi(pinia);
