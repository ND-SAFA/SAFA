<template>
  <stepper-list-step
    title="Integration Sources"
    :item-count="2"
    empty-message=""
  >
    <jira-authentication :inactive="false" @click="emit('input', 'Jira')" />
    <git-hub-authentication
      :inactive="false"
      @click="emit('input', 'GitHub')"
    />
  </stepper-list-step>
</template>

<script lang="ts">
/**
 * Allows for selecting which type of authentication to import from.
 */
export default {
  name: "AuthenticationSelector",
};
</script>

<script setup lang="ts">
import { StepperListStep } from "@/components/common";
import JiraAuthentication from "./JiraAuthentication.vue";
import GitHubAuthentication from "./GitHubAuthentication.vue";

const emit = defineEmits<{
  (e: "input", type: "Jira" | "GitHub"): void;
}>();
</script>
