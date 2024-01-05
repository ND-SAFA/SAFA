<template>
  <typography el="p" :value="ONBOARDING_REPO_SELECT" />

  <git-hub-project-input minimal />

  <flex-box v-if="!!integrationsStore.gitHubProject" t="4" justify="center">
    <text-button outlined label="Continue" @click="handleContinue" />
  </flex-box>
</template>

<script lang="ts">
/**
 * Configures GitHub to import from a repository during onboarding.
 */
export default {
  name: "SelectRepoStep",
};
</script>

<script setup lang="ts">
import { ONBOARDING_REPO_SELECT } from "@/util";
import { integrationsStore, onboardingStore } from "@/hooks";
import { GitHubProjectInput } from "@/components/integrations";
import { Typography, TextButton, FlexBox } from "@/components/common";

/**
 * Handles continuing to the next step.
 */
function handleContinue() {
  onboardingStore.handleNextStep("code");
}
</script>
