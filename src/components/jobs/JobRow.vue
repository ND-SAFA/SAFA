<template>
  <q-tr :props="props.quasarProps" class="cursor-pointer" @click="handleExpand">
    <q-td>
      <icon-button
        tooltip="Toggle expand"
        :icon="props.expanded ? 'down' : 'up'"
        class="q-mr-md"
      />
      <typography :value="props.job.name" />
    </q-td>
    <q-td align="end">
      <typography secondary :value="jobStatus(props.job).progress()" />
    </q-td>
    <q-td align="end">
      <q-chip
        outline
        :color="jobStatus(props.job).color()"
        data-cy="job-status"
      >
        <q-circular-progress
          v-if="jobStatus(props.job).isInProgress()"
          :color="jobStatus(props.job).color()"
          indeterminate
        />
        <icon
          v-else
          :color="jobStatus(props.job).color()"
          :variant="jobStatus(props.job).icon()"
        />
        <typography l="1" :value="jobStatus(props.job).status()" />
      </q-chip>
    </q-td>
  </q-tr>
  <q-tr v-show="props.expanded" :props="props.quasarProps">
    <q-td colspan="100%">
      <stepper minimal dense-labels :model-value="currentStep" :steps="steps" />
      <flex-box full-width justify="end">
        <text-button
          outlined
          label="View Logs"
          r="1"
          data-cy="button-job-log"
          icon="logs"
          @click="handleViewLogs"
        />
        <text-button
          outlined
          label="Delete Upload"
          icon="delete"
          r="1"
          data-cy="button-delete-job"
          @click="handleDelete"
        />
        <text-button
          label="View Project"
          color="primary"
          :disabled="!jobStatus(props.job).isCompleted()"
          data-cy="button-open-job"
          icon="view-tree"
          @click="handleLoad"
        />
      </flex-box>
    </q-td>
  </q-tr>
</template>

<script lang="ts">
/**
 * Displays a row of the job table.
 */
export default {
  name: "JobRow",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { JobSchema, StepperStep } from "@/types";
import { jobStatus } from "@/util";
import { jobStore, logStore, useVModel } from "@/hooks";
import { handleDeleteJob, handleLoadVersion } from "@/api";
import {
  Typography,
  Icon,
  IconButton,
  TextButton,
  FlexBox,
  Stepper,
} from "@/components/common";

const props = defineProps<{
  /**
   * Props passed in from the quasar table.
   */
  quasarProps: Record<string, unknown>;
  /**
   * The job to render.
   */
  job: JobSchema;
  /**
   * Whether the row is expanded.
   */
  expanded: boolean;
}>();

const emit = defineEmits<{
  (e: "update:expanded", expanded: boolean): void;
  (e: "view-logs", job: JobSchema): void;
}>();

const rowExpanded = useVModel(props, "expanded");

const currentStep = computed(() =>
  props.job.currentStep === -1 ? 1 : props.job.currentStep + 1
);
const steps = computed<StepperStep[]>(
  () =>
    props.job.steps?.map((title, idx) => ({
      title,
      done: idx < currentStep.value,
    })) || []
);

/**
 * Opens the view job expansion panel.
 */
function handleExpand(): void {
  jobStore.selectJob(props.job);
  rowExpanded.value = !rowExpanded.value;
}

/**
 * Attempts to delete a job.
 */
function handleDelete(): void {
  handleDeleteJob(props.job, {});
}

/**
 * Displays the log for a job.
 */
async function handleViewLogs(): Promise<void> {
  emit("view-logs", props.job);
}

/**
 * Navigates user to the completed project.
 */
function handleLoad(): void {
  if (props.job.completedEntityId) {
    handleLoadVersion(props.job.completedEntityId);
  } else {
    logStore.onError("Unable to view this project right now.");
  }
}
</script>
