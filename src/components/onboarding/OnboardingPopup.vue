<template>
  <q-dialog
    v-if="userLoggedIn"
    v-model="onboardingStore.open"
    persistent
    maximized
    transition-show="slide-up"
    transition-hide="slide-down"
  >
    <q-card class="bg-background">
      <q-bar class="bg-background q-mt-md">
        <flex-box align="center">
          <icon variant="safa" class="q-mr-md" />
          <typography
            el="h1"
            variant="subtitle"
            secondary
            value="Early Access"
          />
        </flex-box>

        <q-space />

        <flex-box align="center">
          <text-button
            text
            color="primary"
            icon="calendar"
            label="Contact Us"
            style="position: fixed; bottom: 0; right: 0"
            class="q-ma-md"
            @click="onboardingStore.handleScheduleCall(false)"
          />
          <text-button
            text
            icon="graph-refresh"
            label="Restart"
            @click="onboardingApiStore.handleLoadOnboardingState('reset')"
          />
          <text-button
            text
            icon="cancel"
            label="Skip Onboarding"
            @click="onboardingApiStore.handleCloseOnboarding()"
          />
        </flex-box>
      </q-bar>

      <flex-box
        v-if="onboardingStore.loading"
        full-width
        justify="center"
        class="q-pa-lg q-mt-lg"
      >
        <q-spinner-ball class="nav-gradient" size="4em" />
      </flex-box>

      <flex-box
        v-show="!onboardingStore.loading"
        full-width
        justify="center"
        class="q-pa-lg"
      >
        <flex-item parts="6" class="q-ma-md">
          <typography
            align="center"
            el="h1"
            variant="title"
            value="Generate Code Documentation"
          />
          <typography
            align="center"
            el="p"
            secondary
            value="Follow the onboarding steps below to generate documentation for your code."
          />

          <stepper
            v-model="onboardingStore.step"
            vertical
            :steps="onboardingStore.steps"
            hide-actions
            color="gradient"
          >
            <template #1>
              <connect-git-hub-step />
            </template>
            <template #2>
              <select-repo-step />
            </template>
            <template #3>
              <summarize-step />
            </template>
            <template #4>
              <generate-step />
            </template>
          </stepper>
        </flex-item>
        <flex-item v-if="onboardingStore.displayProject" parts="6">
          <project-preview />
        </flex-item>
      </flex-box>
    </q-card>
  </q-dialog>
</template>

<script lang="ts">
/**
 * A popup for initial onboarding to create a user's first project.
 */
export default {
  name: "OnboardingPopup",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { onboardingApiStore, onboardingStore, sessionStore } from "@/hooks";
import {
  TextButton,
  Stepper,
  Typography,
  FlexBox,
  FlexItem,
  Icon,
} from "@/components/common";
import {
  ConnectGitHubStep,
  SelectRepoStep,
  SummarizeStep,
  GenerateStep,
  ProjectPreview,
} from "@/components/onboarding/steps";

const userLoggedIn = computed(() => sessionStore.doesSessionExist);
</script>
