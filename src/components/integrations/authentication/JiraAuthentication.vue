<template>
  <authentication-buttons
    connected-title="Connected to Jira"
    disconnected-title="Connect to Jira"
    :is-loading="isLoading"
    :has-credentials="hasCredentials"
    @click="handleAuthentication"
    @delete="handleDeleteCredentials"
  />
</template>

<script lang="ts">
import Vue from "vue";
import { integrationsStore } from "@/hooks";
import {
  authorizeJira,
  deleteJiraCredentials,
  handleAuthorizeJira,
} from "@/api";
import AuthenticationButtons from "./AuthenticationButtons.vue";

/**
 * Prompts the user to authenticate their Jira account.
 */
export default Vue.extend({
  name: "JiraAuthentication",
  components: {
    AuthenticationButtons,
  },
  data() {
    return {
      isLoading: false,
    };
  },
  /**
   * If a Jira access code is found in the query, loads the Jira authorization token and sites
   * for the user.
   */
  mounted() {
    this.isLoading = true;

    handleAuthorizeJira({
      onComplete: () => (this.isLoading = false),
    });
  },
  computed: {
    /**
     * @return Whether there are current valid credentials.
     */
    hasCredentials(): boolean {
      return integrationsStore.validJiraCredentials;
    },
  },
  methods: {
    /**
     * Opens the Jira authentication window.
     */
    handleAuthentication(): void {
      authorizeJira();
    },
    /**
     * Clears the saved Jira credentials.
     */
    async handleDeleteCredentials(): Promise<void> {
      await deleteJiraCredentials();
      integrationsStore.validJiraCredentials = false;
    },
  },
});
</script>
