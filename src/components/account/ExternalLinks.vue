<template>
  <panel-card title="SAFA Documentation">
    <flex-box full-width align="center" column>
      <text-button text label="Send Feedback" @click="handleFeedback" />
      <text-button text label="Walkthrough" @click="handleWalkthrough" />
      <text-button text label="Recent Changes" @click="handleChangelog" />
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
import { PanelCard, FlexBox, TextButton } from "@/components/common";

/**
 * Routes the user to the feedback page.
 */
function handleFeedback(): void {
  window.open(
    "https://www.notion.so/nd-safa/b73d1a8bfe0345f8b4d72daa1ceaf934?v=6e5d2439907a428fa1db2671a5eaa0b6"
  );
}

/**
 * Routes the user to the walkthrough page.
 */
function handleWalkthrough(): void {
  window.open(
    "https://www.notion.so/nd-safa/8dc14ae706074b099928afe13df39448?v=5b5e744919f84178bac1c96f5a5a92ba"
  );
}

/**
 * Routes the user to the walkthrough page.
 */
function handleChangelog(): void {
  window.open(
    "https://www.notion.so/nd-safa/5155dc357f534eb49f8071a03ce3ae32?v=74f671825a1b4d048909843740c003f1"
  );
}
</script>
