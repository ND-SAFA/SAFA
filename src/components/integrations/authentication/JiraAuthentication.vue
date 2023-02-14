<template>
  <authentication-list-item
    title="Jira"
    :is-loading="isLoading"
    :has-credentials="hasCredentials"
    :inactive="inactive"
    @click="handleClick"
    @connect="handleAuthentication"
    @disconnect="handleDeleteCredentials"
  />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { integrationsStore } from "@/hooks";
import {
  authorizeJira,
  deleteJiraCredentials,
  handleAuthorizeJira,
} from "@/api";
import AuthenticationListItem from "./AuthenticationListItem.vue";

/**
 * Prompts the user to authenticate their Jira account.
 */
export default defineComponent({
  name: "JiraAuthentication",
  components: {
    AuthenticationListItem,
  },
  props: {
    inactive: Boolean,
  },
  data() {
    return {
      isLoading: false,
    };
  },
  computed: {
    /**
     * @return Whether there are current valid credentials.
     */
    hasCredentials(): boolean {
      return integrationsStore.validJiraCredentials;
    },
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
    /**
     * Selects this integration source.
     */
    handleClick(): void {
      this.$emit("click");
    },
  },
});
</script>
