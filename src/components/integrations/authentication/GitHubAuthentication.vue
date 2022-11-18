<template>
  <authentication-buttons
    connected-title="Connected to GitHub"
    disconnected-title="Connect to GitHub"
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
  authorizeGitHub,
  deleteGitHubCredentials,
  handleAuthorizeGitHub,
} from "@/api";
import AuthenticationButtons from "./AuthenticationButtons.vue";

/**
 * Prompts the user to authenticate their GitHub account.
 */
export default Vue.extend({
  name: "GitHubAuthentication",
  components: {
    AuthenticationButtons,
  },
  data() {
    return {
      isLoading: false,
    };
  },
  /**
   * If a GitHub access code is found in the query, loads the GitHub authorization token and sites for the user.
   */
  mounted() {
    this.isLoading = true;

    handleAuthorizeGitHub({
      onComplete: () => (this.isLoading = false),
    });
  },
  computed: {
    /**
     * @return Whether there are current valid credentials.
     */
    hasCredentials(): boolean {
      return integrationsStore.validGitHubCredentials;
    },
  },
  methods: {
    /**
     * Opens the GitHub authentication window.
     */
    handleAuthentication(): void {
      authorizeGitHub();
    },
    /**
     * Clears the saved GitHub credentials.
     */
    async handleDeleteCredentials(): Promise<void> {
      await deleteGitHubCredentials();
      integrationsStore.validGitHubCredentials = false;
    },
  },
});
</script>
