<template>
  <jira-authentication :inactive="false" @click="emit('input', 'Jira')" />
  <git-hub-authentication :inactive="false" @click="emit('input', 'GitHub')" />
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
import JiraAuthentication from "./JiraAuthentication.vue";
import GitHubAuthentication from "./GitHubAuthentication.vue";

const emit = defineEmits<{
  (e: "input", type: "Jira" | "GitHub"): void;
}>();
</script>
