<template>
  <flex-box v-if="appStore.popups.navPanel" x="2" t="3" b="4" justify="center">
    <text-button
      block
      flat
      icon="generate-artifacts"
      label="Generate Docs"
      class="q-py-sm text-gradient bd-gradient"
      @click="handleOnboarding"
    />
  </flex-box>
  <list-item
    v-else
    to=""
    title="Generate Docs"
    icon="generate-artifacts"
    class="text-gradient"
    clickable
    tooltip="Generate Documentation"
    @click="handleOnboarding"
  />
</template>

<script lang="ts">
/**
 * A callout button that opens the onboarding workflow.
 */
export default {
  name: "OnboardingCallout",
};
</script>

<script setup lang="ts">
import { appStore, onboardingApiStore } from "@/hooks";
import { TextButton, FlexBox, ListItem } from "@/components/common";

/**
 * Opens the onboarding workflow.
 */
function handleOnboarding(): void {
  onboardingApiStore.handleLoadOnboardingState("open");
}
</script>
