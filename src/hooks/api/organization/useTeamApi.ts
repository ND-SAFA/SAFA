import { defineStore } from "pinia";

import { useApi } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * A hook for managing requests to the teams API.
 */
export const useOrgApi = defineStore("teamApi", () => {
  const teamApi = useApi("teamApi");
});

export default useOrgApi(pinia);
