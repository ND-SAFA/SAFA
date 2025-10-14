<template>
  <q-tr :props="props.quasarProps" class="cursor-pointer" @click="handleExpand">
    <q-td class="data-table-cell-300">
      <icon-button
        tooltip="Toggle expand"
        :icon="props.expanded ? 'down' : 'up'"
        class="q-mr-md"
      />
      <typography :value="props.job.name" />
    </q-td>
    <q-td align="end">
      <typography
        secondary
        :value="jobStatus(props.job).progress()"
        data-cy="job-progress"
      />
    </q-td>
    <q-td align="end">
      <typography secondary :value="displayTime" data-cy="job-duration" />
    </q-td>
    <q-td align="end">
      <chip outlined :color="jobStatus(props.job).color()" data-cy="job-status">
        <q-circular-progress
          v-if="jobStatus(props.job).isInProgress()"
          :color="jobStatus(props.job).color()"
          indeterminate
        />
        <icon
          v-else
          size="sm"
          :color="jobStatus(props.job).color()"
          :variant="jobStatus(props.job).icon()"
        />
        <typography l="1" :value="jobStatus(props.job).status()" />
      </chip>
    </q-td>
  </q-tr>
  <q-tr v-show="props.expanded" :props="props.quasarProps">
    <q-td colspan="100%">
      <typography variant="caption" :value="props.job.name" />
      <stepper
        minimal
        dense-labels
        hide-actions
        hide-step-back
        :model-value="currentStep"
        :steps="steps"
      />
      <flex-box full-width justify="end" b="2">
        <text-button
          v-if="displayLogs"
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
import { JobRowProps, JobSchema, StepperStep } from "@/types";
import { jobStatus } from "@/util";
import {
  getVersionApiStore,
  jobApiStore,
  jobStore,
  logStore,
  permissionStore,
  useTimeDisplay,
  useVModel,
} from "@/hooks";
import {
  Typography,
  Icon,
  IconButton,
  TextButton,
  FlexBox,
  Stepper,
  Chip,
} from "@/components/common";

const props = defineProps<JobRowProps>();

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

const { displayTime } = useTimeDisplay({
  getStart: () => props.job.startedAt,
  getEnd: () =>
    ["IN_PROGRESS", "COMPLETED"].includes(props.job.status)
      ? props.job.completedAt
      : props.job.lastUpdatedAt,
});

const displayLogs = computed(
  () => permissionStore.isSuperuser || process.env.NODE_ENV !== "production"
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
  jobApiStore.handleDelete(props.job, {});
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
    getVersionApiStore.handleLoad(props.job.completedEntityId);
  } else {
    logStore.onError("Unable to view this project right now.");
  }
}
</script>
