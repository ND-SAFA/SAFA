<template>
  <flex-box
    v-if="ENABLED_FEATURES.GENERATE_ONBOARDING"
    column
    align="center"
    t="2"
  >
    <text-button
      text
      color="gradient"
      class="bd-gradient"
      icon="download"
      :loading="projectApiStore.saveProjectLoading"
      @click="onboardingStore.handleExportProject"
    >
      Export as CSV
    </text-button>
    <flex-box align="center" justify="center" full-width>
      <separator style="width: 40px" />
      <typography secondary el="div" class="q-ma-sm" value="OR" />
      <separator style="width: 40px" />
    </flex-box>
    <text-button
      text
      color="gradient"
      class="bd-gradient"
      icon="view-tree"
      @click="onboardingStore.handleViewProject"
    >
      View in SAFA
    </text-button>
  </flex-box>
  <typography
    v-else
    value="Now that your data has been imported, our team will follow up soon with the generated documentation!"
  />
</template>

<script lang="ts">
/**
 * The last step of onboarding to view the project in SAFA.
 */
export default {
  name: "ViewStep",
};
</script>

<script setup lang="ts">
import { ENABLED_FEATURES } from "@/util";
import { onboardingStore, projectApiStore } from "@/hooks";
import { FlexBox, Separator, TextButton, Typography } from "@/components";
</script>
