<template>
  <v-container class="d-flex justify-center">
    <v-btn
      large
      color="primary"
      :disabled="isDisabled"
      :loading="isLoading"
      @click="handleAuthentication"
    >
      <v-icon class="mr-1">mdi-transit-connection-variant</v-icon>
      <span v-if="!hasCredentials">Connect to GitHub</span>
      <span v-else>Connected to GitHub</span>
    </v-btn>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { authorizeGitHub } from "@/api";

/**
 * Prompts the user to authenticate their Jira account.
 */
export default Vue.extend({
  name: "JiraAuthentication",
  props: {
    hasCredentials: Boolean,
    isLoading: Boolean,
  },
  methods: {
    handleAuthentication(): void {
      authorizeGitHub();
    },
  },
  computed: {
    /**
     * Returns whether the button is enabled.
     */
    isDisabled(): boolean {
      return this.hasCredentials || this.isLoading;
    },
  },
});
</script>
