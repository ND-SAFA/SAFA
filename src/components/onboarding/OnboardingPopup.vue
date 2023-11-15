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

        <text-button text icon="cancel" @click="handleClose">
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
                  color="gradient"
                  class="bd-gradient"
                  icon="generate-artifacts"
                  :disabled="error"
                  @click="handleGenerate"
                >
                  Generate Documentation
                </text-button>
              </flex-box>
              <q-banner v-if="error" rounded class="bg-background q-mt-md">
                <template #avatar>
                  <icon
                    variant="error"
                    color="secondary"
                    size="md"
                    class="q-mr-sm"
                  />
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
                    @click="handleScheduleCall"
                  >
                    Schedule a Call
                  </text-button>
                </template>
              </q-banner>
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
                color="gradient"
                class="bd-gradient"
                icon="download"
                :loading="projectApiStore.saveProjectLoading"
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
import { LocalStorageKeys, StepperStep } from "@/types";
import {
  ARTIFACT_GENERATION_TYPES,
  ENABLED_FEATURES,
  ONBOARDING_STEPS,
} from "@/util";
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

const open = ref(false);
const error = ref(false);

const step = ref(1);
const steps = ref<StepperStep[]>(
  Object.values(ONBOARDING_STEPS).map((step) => ({ ...step, done: false }))
);

const generationTypes = ref([
  ARTIFACT_GENERATION_TYPES.USER_STORY,
  ARTIFACT_GENERATION_TYPES.SUB_SYSTEM,
]);

const userLoggedIn = computed(() => sessionStore.doesSessionExist);

const recentJob = computed(() =>
  steps.value[ONBOARDING_STEPS.generate.index].done
    ? jobStore.jobs[0]
    : undefined
);
const jobProgressDisplay = computed(() =>
  recentJob.value
    ? `Step ${recentJob.value.currentStep + 1} of ${
        recentJob.value.steps.length
      }: ${recentJob.value.steps[recentJob.value.currentStep]}`
    : ""
);

/**
 * Close the popup and mark onboarding as complete.
 */
function handleClose() {
  open.value = false;
  localStorage.setItem(LocalStorageKeys.onboarding, "true");
}

/**
 * Schedule a call with the SAFA team.
 */
function handleScheduleCall() {
  // TODO
}

/**
 * Generate documentation for the selected project.
 * - Moves from Generate Documentation step if a project is created.
 */
function handleGenerate() {
  if (ENABLED_FEATURES.ONBOARDING_MOCKED) {
    steps.value[ONBOARDING_STEPS.generate.index].done = true;
    step.value = ONBOARDING_STEPS.job.number;

    setTimeout(() => {
      steps.value[ONBOARDING_STEPS.job.index].done = true;
      step.value = ONBOARDING_STEPS.view.number;
    }, 2000);

    return;
  }

  createProjectApiStore.handleGitHubImport({
    onSuccess: () => {
      steps.value[ONBOARDING_STEPS.generate.index].done = true;
      step.value = ONBOARDING_STEPS.job.number;
    },
    onError: () => (error.value = true),
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
  handleClose();
}

/**
 * View the selected project in SAFA.
 */
async function handleViewProject() {
  if (!recentJob.value?.completedEntityId) return;

  await getVersionApiStore.handleLoadCurrent({
    projectId: recentJob.value.completedEntityId,
  });

  handleClose();
}

// Preload GitHub projects if credentials are already set.
onMounted(() => {
  const storedOnboardingComplete =
    localStorage.getItem(LocalStorageKeys.onboarding) === "true";

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
      steps.value[ONBOARDING_STEPS.connect.index].done = true;

      if (step.value === ONBOARDING_STEPS.connect.number) {
        step.value = ONBOARDING_STEPS.code.number;
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
      steps.value[ONBOARDING_STEPS.code.index].done = true;

      if (step.value === ONBOARDING_STEPS.code.number) {
        step.value = ONBOARDING_STEPS.generate.number;
      }
    }
  }
);

// Move from Await Generation step if the job completes.
watch(
  () => recentJob.value?.status,
  (status) => {
    if (status !== "COMPLETED") return;

    steps.value[ONBOARDING_STEPS.generate.index].done = true;

    if (step.value === ONBOARDING_STEPS.generate.number) {
      step.value = ONBOARDING_STEPS.job.number;
    }
  }
);
</script>
