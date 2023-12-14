<template>
  <q-dialog
    v-if="userLoggedIn"
    v-model="onboardingStore.open"
    persistent
    maximized
    transition-show="slide-up"
    transition-hide="slide-down"
  >
    <q-card>
      <q-bar class="bg-neutral q-mt-md">
        <q-space />

        <text-button text icon="cancel" @click="onboardingStore.handleClose">
          Skip Onboarding
        </text-button>
      </q-bar>

      <flex-box full-width justify="center" class="q-pa-lg q-mt-10">
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
import { computed, onMounted, watch } from "vue";
import {
  gitHubApiStore,
  integrationsStore,
  onboardingStore,
  permissionStore,
  sessionStore,
} from "@/hooks";
import { TextButton, Stepper, Typography, FlexBox } from "@/components/common";
import {
  ConnectGitHubStep,
  SelectRepoStep,
  SummarizeStep,
  GenerateStep,
  ProjectPreview,
} from "@/components/onboarding/steps";
import FlexItem from "@/components/common/display/content/FlexItem.vue";

const userLoggedIn = computed(() => sessionStore.doesSessionExist);

// Preload GitHub projects if credentials are already set.
onMounted(async () => {
  await onboardingStore.handleReload();
});

// Open the popup when the user logs in, if they have not already completed it.
watch(
  () => userLoggedIn.value,
  (userLoggedIn) => {
    if (
      userLoggedIn &&
      !onboardingStore.isComplete &&
      !permissionStore.isDemo
    ) {
      onboardingStore.open = true;
    }
  }
);

// Move from Connect GitHub step if credentials are set.
watch(
  () => integrationsStore.validGitHubCredentials,
  (valid) => {
    if (!valid) return;

    onboardingStore.handleNextStep("connect");
    gitHubApiStore.handleLoadProjects();
  }
);
</script>
