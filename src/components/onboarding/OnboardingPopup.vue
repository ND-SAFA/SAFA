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
                v-for="type in onboardingStore.generationTypes"
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
                  :disabled="onboardingStore.error"
                  @click="onboardingStore.handleGenerate"
                >
                  Generate Documentation
                </text-button>
              </flex-box>
              <q-banner
                v-if="onboardingStore.error"
                rounded
                class="bg-background q-mt-md"
              >
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
                    @click="onboardingStore.handleScheduleCall"
                  >
                    Schedule a Call
                  </text-button>
                </template>
              </q-banner>
            </flex-box>
          </template>
          <template v-if="!!uploadedJob" #4>
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
              :title="uploadedJob.name"
              :subtitle="onboardingStore.uploadProgress"
            >
              <template #icon>
                <q-circular-progress
                  v-if="uploadedJob.status === 'IN_PROGRESS'"
                  color="gradient"
                  indeterminate
                  size="md"
                />
                <icon
                  v-else-if="uploadedJob.status === 'COMPLETED'"
                  variant="job-complete"
                  color="primary"
                  size="md"
                />
                <icon
                  v-else-if="uploadedJob.status === 'FAILED'"
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
