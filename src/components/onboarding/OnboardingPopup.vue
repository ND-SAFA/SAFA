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

        <stepper v-model="step" vertical :steps="steps" hide-actions>
          <template #1>
            <git-hub-authentication inactive />
          </template>
          <template #2>
            <git-hub-project-input />
          </template>
          <template #3>
            <flex-box column align="center" t="2">
              <typography el="div" value="Importing from GitHub:" />
              <attribute-chip
                :value="integrationsStore.gitHubProject?.name || ''"
                icon="project-add"
                color="primary"
              />
              <typography el="div" value="Generating Documents:" />
              <attribute-chip
                v-for="type in generationTypes"
                :key="type"
                :value="type"
                icon="create-artifact"
                color="primary"
              />
              <!-- TODO: confirm data generation cost estimate, pay with stripe -->
              <flex-box t="4">
                <text-button
                  text
                  large
                  color="gradient"
                  class="bd-gradient"
                  icon="generate-artifacts"
                  @click="handleGenerate"
                >
                  Generate Documentation
                </text-button>
              </flex-box>
            </flex-box>
          </template>
          <template v-if="!!recentJob" #4>
            <typography
              el="p"
              value="
                You will receive an email when generation completes.
                This process takes a few minutes for 20 code files, and around 30 minutes for 100 code files.
              "
            />
            <!-- TODO: handle errors with followup call -->
            <list-item
              dense
              :title="recentJob.name"
              :subtitle="jobProgressDisplay"
            >
              <template #icon>
                <q-circular-progress
                  v-if="recentJob.status === 'IN_PROGRESS'"
                  color="gradient"
                  indeterminate
                  size="md"
                />
                <icon
                  v-else-if="recentJob.status === 'COMPLETED'"
                  variant="job-complete"
                  color="primary"
                  size="md"
                />
                <icon
                  v-else-if="recentJob.status === 'FAILED'"
                  variant="job-fail"
                  color="error"
                  size="md"
                />
              </template>
            </list-item>
          </template>
          <template v-else #4>
            <flex-box justify="center">
              <q-circular-progress color="primary" indeterminate size="md" />
            </flex-box>
          </template>
          <template #5>
            <flex-box column align="center" t="2">
              <text-button
                text
                large
                color="gradient"
                class="bd-gradient"
                icon="download"
                @click="handleExportProject"
              >
                Export as CSV
              </text-button>
              <flex-box align="center" justify="center" full-width>
                <separator style="width: 40px" />
                <typography el="div" class="q-ma-sm" value="OR" />
                <separator style="width: 40px" />
              </flex-box>
              <text-button
                text
                large
                color="gradient"
                class="bd-gradient"
                icon="view-tree"
                @click="handleViewProject"
              >
                View in SAFA
              </text-button>
            </flex-box>
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
import { ARTIFACT_GENERATION_TYPES, ENABLED_FEATURES } from "@/util";
import {
  createProjectApiStore,
  getVersionApiStore,
  gitHubApiStore,
  integrationsStore,
  jobApiStore,
  jobStore,
  logStore,
  projectApiStore,
  sessionStore,
} from "@/hooks";
import {
  TextButton,
  Stepper,
  Typography,
  FlexBox,
  AttributeChip,
  ListItem,
  Icon,
  Separator,
} from "@/components/common";
import {
  GitHubAuthentication,
  GitHubProjectInput,
} from "@/components/integrations";

const stepMap = {
  connect: {
    title: "Connect GitHub",
    caption: "Connect your GitHub account to get started.",
    index: 0,
    number: 1,
  },
  code: {
    title: "Select Repository",
    caption: "Select code from GitHub to import.",
    index: 1,
    number: 2,
  },
  generate: {
    title: "Generate Documentation",
    caption: ENABLED_FEATURES.BILLING_ONBOARDING
      ? "Review costs and generate documentation for your code."
      : "Generate documentation for your code.",
    index: 2,
    number: 3,
  },
  job: {
    title: "Await Generation",
    caption: "Wait for data generation to complete.",
    index: 3,
    number: 4,
  },
  view: {
    title: "View Documentation",
    caption: "Export generated data, or view the data within SAFA.",
    index: 4,
    number: 5,
  },
};

const open = ref(false);

const step = ref(1);
const steps = ref<StepperStep[]>(
  Object.values(stepMap).map((step) => ({ ...step, done: false }))
);

const generationTypes = ref([
  ARTIFACT_GENERATION_TYPES.USER_STORY,
  ARTIFACT_GENERATION_TYPES.SUB_SYSTEM,
]);

const userLoggedIn = computed(() => sessionStore.doesSessionExist);

const recentJob = computed(() =>
  steps.value[stepMap.generate.index].done ? jobStore.jobs[0] : undefined
);
const jobProgressDisplay = computed(() =>
  recentJob.value
    ? `Step ${recentJob.value.currentStep + 1} of ${
        recentJob.value.steps.length
      }: ${recentJob.value.steps[recentJob.value.currentStep]}`
    : ""
);

/**
 * Generate documentation for the selected project.
 * - Moves from Generate Documentation step if a project is created.
 */
function handleGenerate() {
  if (ENABLED_FEATURES.ONBOARDING_MOCKED) {
    steps.value[stepMap.generate.index].done = true;
    step.value = stepMap.job.number;

    setTimeout(() => {
      steps.value[stepMap.job.index].done = true;
      step.value = stepMap.view.number;
    }, 2000);

    return;
  }

  createProjectApiStore.handleGitHubImport({
    onSuccess: () => {
      steps.value[stepMap.generate.index].done = true;
      step.value = stepMap.job.number;
    },
    // onError: () => {},
    // onComplete: () => {},
  });
}

/**
 * Export the selected project as a CSV.
 */
async function handleExportProject() {
  if (!recentJob.value?.completedEntityId) return;

  await getVersionApiStore.handleLoadCurrent({
    projectId: recentJob.value.completedEntityId,
  });

  await projectApiStore.handleDownload(
    "csv",
    recentJob.value.completedEntityId
  );

  logStore.onSuccess("Your data is being exported.");
}

/**
 * View the selected project in SAFA.
 */
async function handleViewProject() {
  if (!recentJob.value?.completedEntityId) return;

  await getVersionApiStore.handleLoadCurrent({
    projectId: recentJob.value.completedEntityId,
  });

  open.value = false;
}

// Preload GitHub projects if credentials are already set.
onMounted(() => {
  if (integrationsStore.validGitHubCredentials) {
    gitHubApiStore.handleLoadProjects();
  }

  jobApiStore.handleReload();
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

// Move from Connect GitHub step if credentials are set.
watch(
  () => integrationsStore.validGitHubCredentials,
  (valid) => {
    if (valid) {
      steps.value[stepMap.connect.index].done = true;

      if (step.value === stepMap.connect.number) {
        step.value = stepMap.code.number;
      }

      gitHubApiStore.handleLoadProjects();
    }
  }
);

// Move from Generate Data step if repo is selected.
watch(
  () => !!integrationsStore.gitHubProject,
  (valid) => {
    if (valid) {
      steps.value[stepMap.code.index].done = true;

      if (step.value === stepMap.code.number) {
        step.value = stepMap.generate.number;
      }
    }
  }
);

// Move from Await Generation step if the job completes.
watch(
  () => recentJob.value?.status,
  (status) => {
    if (status !== "COMPLETED") return;

    steps.value[stepMap.generate.index].done = true;

    if (step.value === stepMap.generate.number) {
      step.value = stepMap.job.number;
    }
  }
);
</script>
