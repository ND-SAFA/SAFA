<template>
  <authentication-list-item
    title="GitHub"
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
 * Prompts the user to authenticate their GitHub account.
 */
export default {
  name: "GitHubAuthentication",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { integrationsStore } from "@/hooks";
import {
  authorizeGitHub,
  deleteGitHubCredentials,
  handleAuthorizeGitHub,
} from "@/api";
import AuthenticationListItem from "./AuthenticationListItem.vue";

const props = defineProps<{
  inactive?: boolean;
}>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const loading = ref(false);

const hasCredentials = computed(() => integrationsStore.validGitHubCredentials);

/**
 * Opens the GitHub authentication window.
 */
function handleAuthentication(): void {
  authorizeGitHub();
}

/**
 * Clears the saved GitHub credentials.
 */
async function handleDeleteCredentials(): Promise<void> {
  await deleteGitHubCredentials();
  integrationsStore.validGitHubCredentials = false;
}

onMounted(() => {
  loading.value = true;

  handleAuthorizeGitHub({
    onComplete: () => (loading.value = false),
  });
});
</script>
