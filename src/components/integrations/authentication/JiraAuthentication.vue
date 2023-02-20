<template>
  <authentication-list-item
    title="Jira"
    :loading="loading"
    :has-credentials="hasCredentials"
    :inactive="props.inactive"
    @click="emit('click')"
    @connect="handleAuthentication"
    @disconnect="handleDeleteCredentials"
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
import { computed, onMounted, ref } from "vue";
import { integrationsStore } from "@/hooks";
import {
  authorizeJira,
  deleteJiraCredentials,
  handleAuthorizeJira,
} from "@/api";
import AuthenticationListItem from "./AuthenticationListItem.vue";

const props = defineProps<{
  inactive?: boolean;
}>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const loading = ref(false);

const hasCredentials = computed(() => integrationsStore.validJiraCredentials);

/**
 * Opens the Jira authentication window.
 */
function handleAuthentication(): void {
  authorizeJira();
}

/**
 * Clears the saved Jira credentials.
 */
async function handleDeleteCredentials(): Promise<void> {
  await deleteJiraCredentials();
  integrationsStore.validJiraCredentials = false;
}

onMounted(() => {
  loading.value = true;

  handleAuthorizeJira({
    onComplete: () => (loading.value = false),
  });
});
</script>
