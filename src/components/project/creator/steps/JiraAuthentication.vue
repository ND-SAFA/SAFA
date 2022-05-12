<template>
  <v-container class="d-flex justify-center">
    <v-btn
      large
      color="primary"
      :disabled="isDisabled"
      :loading="isLoading"
      @click="handleJiraAuthentication"
    >
      <v-icon class="mr-1">mdi-transit-connection-variant</v-icon>
      <span v-if="!token">Connect to Jira</span>
      <span v-else>Connected to Jira</span>
    </v-btn>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { authorizeJira } from "@/api";

/**
 * Prompts the user to authenticate their Jira account.
 */
export default Vue.extend({
  name: "JiraAuthentication",
  props: {
    token: {
      type: String,
      required: true,
    },
    isLoading: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    /**
     * Opens the jira authentication window.
     */
    handleJiraAuthentication(): void {
      authorizeJira();
    },
  },
  computed: {
    /**
     * Returns whether the button is enabled.
     */
    isDisabled(): boolean {
      return !!this.token || this.isLoading;
    },
  },
});
</script>
