<template>
  <typography el="p" :value="ONBOARDING_GITHUB_IMPORT" />

  <git-hub-authentication inactive />

  <callout-sub-step icon="security" :message="ONBOARDING_GITHUB_SECURITY">
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
  </callout-sub-step>
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
import { TextButton, Typography } from "@/components";
import CalloutSubStep from "./CalloutSubStep.vue";

/**
 * Opens the security practices link in a new tab.
 */
function handleViewSecurityPractices() {
  window.open(SECURITY_LINK);
}
</script>
