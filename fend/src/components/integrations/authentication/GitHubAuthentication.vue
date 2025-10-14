<template>
  <authentication-list-item
    title="GitHub"
    :loading="gitHubApiStore.loading"
    :has-credentials="hasCredentials"
    :inactive="props.inactive"
    @click="emit('click')"
    @connect="gitHubApiStore.handleAuthRedirect"
    @disconnect="gitHubApiStore.handleDeleteCredentials"
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
import { computed, onMounted } from "vue";
import { AuthenticationListItemProps } from "@/types";
import { gitHubApiStore, integrationsStore } from "@/hooks";
import AuthenticationListItem from "./AuthenticationListItem.vue";

const props = defineProps<Pick<AuthenticationListItemProps, "inactive">>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const hasCredentials = computed(() => integrationsStore.validGitHubCredentials);

onMounted(() => {
  gitHubApiStore.handleVerifyCredentials();
});
</script>
