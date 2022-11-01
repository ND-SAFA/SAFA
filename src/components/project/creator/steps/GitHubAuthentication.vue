<template>
  <generic-stepper-authentication
    connected-title="Connected to GitHub"
    disconnected-title="Connect to GitHub"
    :is-loading="isLoading"
    :has-credentials="hasCredentials"
    @click="handleAuthentication"
    @delete="$emit('delete')"
  />
</template>

<script lang="ts">
import Vue from "vue";
import { authorizeGitHub } from "@/api";
import { GenericStepperAuthentication } from "@/components";

/**
 * Prompts the user to authenticate their Jira account.
 *
 * @emits-1 - `delete` - On credentials delete.
 */
export default Vue.extend({
  name: "GitHubAuthentication",
  components: {
    GenericStepperAuthentication,
  },
  props: {
    hasCredentials: Boolean,
    isLoading: Boolean,
  },
  methods: {
    handleAuthentication(): void {
      authorizeGitHub();
    },
  },
});
</script>
