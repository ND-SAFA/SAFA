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

      <div class="q-mx-auto q-mt-10" style="width: 700px; margin-top: 100px">
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
            <select-repo-step />
          </template>
          <template #2>
            <git-hub-project-input />
          </template>
          <template #3>
            <generate-step />
          </template>
          <template #4>
            <await-generate-step />
          </template>
          <template #5>
            <view-step />
          </template>
        </stepper>
      </div>
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
import { ENABLED_FEATURES } from "@/util";
import {
  gitHubApiStore,
  integrationsStore,
  onboardingStore,
  permissionStore,
  sessionStore,
} from "@/hooks";
import { TextButton, Stepper, Typography } from "@/components/common";
import { GitHubProjectInput } from "@/components/integrations";
import {
  SelectRepoStep,
  ViewStep,
  GenerateStep,
  AwaitGenerateStep,
} from "@/components/onboarding/steps";

const userLoggedIn = computed(() => sessionStore.doesSessionExist);
const uploadedJob = computed(() => onboardingStore.uploadedJob);

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
      !permissionStore.isDemo &&
      ENABLED_FEATURES.ONBOARDING
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

// Move from Generate Data step if repo is selected.
watch(
  () => !!integrationsStore.gitHubProject,
  (valid) => {
    if (!valid) return;

    onboardingStore.handleNextStep("code");
  }
);

// Move from Await Generation step if the job completes.
watch(
  () => uploadedJob.value?.status,
  (status) => {
    if (status !== "COMPLETED") return;

    onboardingStore.handleNextStep("job");
  }
);
</script>
