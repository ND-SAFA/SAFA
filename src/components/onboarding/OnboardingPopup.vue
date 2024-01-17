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
        <q-space />

        <text-button text icon="cancel" @click="onboardingStore.handleClose">
          Skip Onboarding
        </text-button>
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
              <generate-step v-if="ENABLED_FEATURES.ONBOARDING_GENERATE" />
              <typography
                v-else
                value="
                  Now that your data has been imported, our team will run SAFA's document generation ASAP!
                  Check back soon to see your generated documentation.
                "
              />
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
import { computed, watch } from "vue";
import { ENABLED_FEATURES } from "@/util";
import { onboardingStore, permissionStore, sessionStore } from "@/hooks";
import {
  TextButton,
  Stepper,
  Typography,
  FlexBox,
  FlexItem,
} from "@/components/common";
import {
  ConnectGitHubStep,
  SelectRepoStep,
  SummarizeStep,
  GenerateStep,
  ProjectPreview,
} from "@/components/onboarding/steps";

const userLoggedIn = computed(() => sessionStore.doesSessionExist);

// Check the onboarding workflow status when the user logs in, and open the popup if it's not complete.
watch(
  () => userLoggedIn.value,
  async (userLoggedIn) => {
    if (!userLoggedIn || permissionStore.isDemo) return;

    await onboardingStore.handleReload();
  }
);
</script>
