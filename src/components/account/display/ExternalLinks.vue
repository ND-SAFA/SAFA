<template>
  <panel-card title="SAFA Documentation">
    <flex-box full-width justify="center">
      <flex-box column>
        <text-button
          text
          color="gradient"
          label="Generate Docs"
          icon="generate-artifacts"
          @click="handleOnboarding"
        />
        <text-button
          text
          label="About SAFA"
          icon="nav-artifact"
          @click="handleWalkthrough"
        />
        <text-button
          text
          label="Send Feedback"
          icon="feedback"
          @click="handleFeedback"
        />
        <text-button
          text
          label="Recent Changes"
          icon="changelog"
          @click="handleChangelog"
        />
      </flex-box>
    </flex-box>
  </panel-card>
</template>

<script lang="ts">
/**
 * Provides links to external documentation.
 */
export default {
  name: "ExternalLinks",
};
</script>

<script setup lang="ts">
import { ABOUT_SAFA_LINK, CHANGELOG_LINK, FEEDBACK_LINK } from "@/util";
import { onboardingApiStore } from "@/hooks";
import { PanelCard, FlexBox, TextButton } from "@/components/common";

/**
 * Opens the onboarding workflow.
 */
function handleOnboarding(): void {
  onboardingApiStore.handleLoadOnboardingState("open");
}

/**
 * Routes the user to the feedback page.
 */
function handleFeedback(): void {
  window.open(FEEDBACK_LINK);
}

/**
 * Routes the user to the walkthrough page.
 */
function handleWalkthrough(): void {
  window.open(ABOUT_SAFA_LINK);
}

/**
 * Routes the user to the walkthrough page.
 */
function handleChangelog(): void {
  window.open(CHANGELOG_LINK);
}
</script>
