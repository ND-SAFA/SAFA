<template>
  <typography el="p" :value="ONBOARDING_GITHUB_IMPORT" />

  <git-hub-authentication inactive />

  <q-banner rounded class="bd-secondary q-mt-md">
    <template #avatar>
      <icon variant="security" color="secondary" size="md" />
    </template>
    <typography :value="ONBOARDING_GITHUB_SECURITY" />
    <template #action>
      <text-button
        text
        color="secondary"
        icon="changelog"
        @click="handleViewSecurityPractices"
      >
        Security Practices
      </text-button>
    </template>
  </q-banner>
</template>

<script lang="ts">
/**
 * Connects to GitHub to import code during onboarding.
 */
export default {
  name: "ConnectGitHubStep",
};
</script>

<script setup lang="ts">
import {
  ONBOARDING_GITHUB_IMPORT,
  ONBOARDING_GITHUB_SECURITY,
  SECURITY_LINK,
} from "@/util";
import { GitHubAuthentication } from "@/components/integrations";
import { Icon, TextButton, Typography } from "@/components";

/**
 * Opens the security practices link in a new tab.
 */
function handleViewSecurityPractices() {
  window.open(SECURITY_LINK);
}
</script>
