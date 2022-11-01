<template>
  <generic-stepper-authentication
    connected-title="Connected to Jira"
    disconnected-title="Connect to Jira"
    :is-loading="isLoading"
    :has-credentials="hasCredentials"
    @click="handleJiraAuthentication"
    @delete="$emit('delete')"
  />
</template>

<script lang="ts">
import Vue from "vue";
import { authorizeJira } from "@/api";
import { GenericStepperAuthentication } from "@/components";

/**
 * Prompts the user to authenticate their Jira account.
 *
 * @emits-1 - `delete` - On credentials delete.
 */
export default Vue.extend({
  name: "JiraAuthentication",
  components: {
    GenericStepperAuthentication,
  },
  props: {
    hasCredentials: {
      type: Boolean,
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
});
</script>
