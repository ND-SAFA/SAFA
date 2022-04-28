<template>
  <v-container class="d-flex justify-center">
    <v-btn
      large
      color="primary"
      :disabled="!!token"
      @click="handleAuthentication"
    >
      <v-icon class="mr-1">mdi-transit-connection-variant</v-icon>
      <span v-if="!token">Connect to GitHub</span>
      <span v-else>Connected to GitHub</span>
    </v-btn>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { logModule } from "@/store";

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
    handleAuthentication(): void {
      logModule.onInfo("Importing from GitHub is not yet enabled.");
    },
  },
});
</script>
