import { defineStore } from "pinia";

import { pinia } from "@/plugins";

/**
 * This module defines the state of 3rd party integrations.
 */
export const useIntegrations = defineStore("integrations", {
  state: () => ({
    /**
     * Whether this user is connected to Jira.
     */
    validJiraCredentials: false,
    /**
     * Whether this user is connected to GitHub.
     */
    validGitHubCredentials: false,
  }),
  getters: {},
  actions: {},
});

export default useIntegrations(pinia);
