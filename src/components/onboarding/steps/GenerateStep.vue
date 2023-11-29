<template>
  <flex-box column align="center" t="2">
    <typography el="div" value="Importing from GitHub:" />
    <attribute-chip
      :value="integrationsStore.gitHubProject?.name || ''"
      icon="project-add"
      color="primary"
    />
    <template v-if="ENABLED_FEATURES.GENERATE_ONBOARDING">
      <typography el="div" value="Generating Documents:" />
      <attribute-chip
        v-for="type in onboardingStore.generationTypes"
        :key="type"
        :value="type"
        icon="create-artifact"
        color="primary"
      />
    </template>
    <!-- TODO: confirm data generation cost estimate, pay with stripe -->
    <flex-box t="4">
      <text-button
        text
        color="gradient"
        class="bd-gradient"
        icon="generate-artifacts"
        :disabled="onboardingStore.error"
        @click="onboardingStore.handleGenerate"
      >
        {{ onboardingStore.steps[2].title }}
      </text-button>
    </flex-box>
    <q-banner
      v-if="onboardingStore.error"
      rounded
      class="bg-background q-mt-md"
    >
      <template #avatar>
        <icon variant="error" color="secondary" size="md" class="q-mr-sm" />
      </template>
      <typography
        value="
          On no! It looks like there was an issue with importing from GitHub.
          You can schedule a call with us below to ensure your data gets uploaded properly.
        "
      />
      <template #action>
        <text-button
          text
          color="secondary"
          icon="calendar"
          @click="onboardingStore.handleScheduleCall"
        >
          Schedule a Call
        </text-button>
      </template>
    </q-banner>
  </flex-box>
</template>

<script lang="ts">
/**
 * The onboarding step to generate data.
 */
export default {
  name: "GenerateStep",
};
</script>

<script setup lang="ts">
import { ENABLED_FEATURES } from "@/util";
import { integrationsStore, onboardingStore } from "@/hooks";
import {
  AttributeChip,
  FlexBox,
  Icon,
  TextButton,
  Typography,
} from "@/components";
</script>
