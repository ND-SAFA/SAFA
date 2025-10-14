<template>
  <authentication-list-item
    title="Jira"
    :loading="jiraApiStore.loading"
    :has-credentials="hasCredentials"
    :inactive="props.inactive"
    @click="emit('click')"
    @connect="jiraApiStore.handleAuthRedirect"
    @disconnect="jiraApiStore.handleDeleteCredentials"
  />
</template>

<script lang="ts">
/**
 * Prompts the user to authenticate their Jira account.
 */
export default {
  name: "JiraAuthentication",
};
</script>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import { AuthenticationListItemProps } from "@/types";
import { integrationsStore, jiraApiStore } from "@/hooks";
import AuthenticationListItem from "./AuthenticationListItem.vue";

const props = defineProps<Pick<AuthenticationListItemProps, "inactive">>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const hasCredentials = computed(() => integrationsStore.validJiraCredentials);

onMounted(() => {
  jiraApiStore.handleVerifyCredentials();
});
</script>
