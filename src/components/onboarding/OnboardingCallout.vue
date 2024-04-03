<template>
  <flex-box x="2" y="2" justify="center">
    <text-button
      v-if="appStore.popups.navPanel"
      block
      icon="onboarding"
      color="primary"
      label="Generate Now"
      class="q-py-sm"
      @click="handleOnboarding"
    />
    <icon-button
      v-else
      tooltip="Generate Now"
      icon="onboarding"
      color="primary"
      @click="handleOnboarding"
    />
  </flex-box>
</template>

<script lang="ts">
/**
 * A substep in the onboarding process that displays a callout message.
 */
export default {
  name: "OnboardingCallout",
};
</script>

<script setup lang="ts">
import { appStore, onboardingApiStore } from "@/hooks";
import { IconButton, TextButton, FlexBox } from "@/components/common";

/**
 * Opens the onboarding workflow.
 */
function handleOnboarding(): void {
  onboardingApiStore.handleLoadOnboardingState("open");
}
</script>
