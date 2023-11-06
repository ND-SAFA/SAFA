<template>
  <q-dialog
    v-if="userLoggedIn"
    v-model="open"
    persistent
    maximized
    transition-show="slide-up"
    transition-hide="slide-down"
  >
    <q-card>
      <q-bar class="bg-neutral q-mt-md">
        <q-space />

        <text-button v-close-popup text icon="cancel">
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

        <stepper v-model="step" vertical :steps="steps">
          <template #1>
            <git-hub-authentication inactive />
          </template>
          <template #2>
            <git-hub-project-input />
          </template>
          <template #3>
            [confirm docs to generate, confirm data generation cost estimate,
            pay with stripe]
            <flex-box justify="center">
              <text-button text color="gradient" @click="handleGenerate">
                Generate Documentation
              </text-button>
            </flex-box>
          </template>
          <template #4>
            [wait for generation job to complete, express whether job was
            successful or not & whether payment went through]
          </template>
          <template #5>
            [Easily export docs as file download, or view within SAFA]
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
import { computed, onMounted, ref, watch } from "vue";
import { StepperStep } from "@/types";
import { ENABLED_FEATURES } from "@/util";
import {
  createProjectApiStore,
  gitHubApiStore,
  integrationsStore,
  sessionStore,
} from "@/hooks";
import { TextButton, Stepper, Typography, FlexBox } from "@/components/common";
import {
  GitHubAuthentication,
  GitHubProjectInput,
} from "@/components/integrations";

const open = ref(false);

const step = ref(1);
const steps = ref<StepperStep[]>([
  {
    title: "Connect GitHub",
    caption: "Connect your GitHub account to get started.",
    done: false,
  },
  {
    title: "Select Repository",
    caption: "Select code from GitHub to import.",
    done: false,
  },
  {
    title: "Generate Documentation",
    caption: ENABLED_FEATURES.BILLING_ONBOARDING
      ? "Review costs and generate documentation for your code."
      : "Generate documentation for your code.",
    done: false,
  },
  {
    title: "Await Generation",
    caption: "Wait for data generation to complete.",
    done: false,
  },
  {
    title: "View Documentation",
    caption: "Export generated data, or view the data within SAFA.",
    done: false,
  },
]);

const userLoggedIn = computed(() => sessionStore.doesSessionExist);

/**
 * Generate documentation for the selected project.
 */
function handleGenerate() {
  createProjectApiStore.handleGitHubImport({
    // onSuccess: () => {},
    // onError: () => {},
    // onComplete: () => {},
    onSuccess: () => {
      steps.value[2].done = true;
      step.value = 4;
    },
  });
}

// Preload GitHub projects if credentials are already set.
onMounted(() => {
  if (integrationsStore.validGitHubCredentials) {
    gitHubApiStore.handleLoadProjects();
  }
});

// Open the popup when the user logs in, if they have not already completed it.
watch(
  () => userLoggedIn.value,
  (userLoggedIn) => {
    if (userLoggedIn && ENABLED_FEATURES.ONBOARDING) {
      open.value = true;
    }
  }
);

// Move from GitHub connect step if credentials are set.
watch(
  () => integrationsStore.validGitHubCredentials,
  (valid) => {
    if (valid) {
      steps.value[0].done = true;

      if (step.value === 1) {
        step.value = 2;
      }

      gitHubApiStore.handleLoadProjects();
    }
  }
);

// Move from GitHub repo step if repo is selected.
watch(
  () => !!integrationsStore.gitHubProject,
  (valid) => {
    if (valid) {
      steps.value[1].done = true;

      if (step.value === 2) {
        step.value = 3;
      }
    }
  }
);
</script>
