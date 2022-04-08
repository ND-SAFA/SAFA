<template>
  <v-container class="d-flex justify-center">
    <v-btn
      large
      class="my-10"
      color="primary"
      :disabled="!!token"
      @click="handleJiraAuthentication"
    >
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
  },
  methods: {
    handleJiraAuthentication(): void {
      authorizeJira();
    },
  },
});
</script>
