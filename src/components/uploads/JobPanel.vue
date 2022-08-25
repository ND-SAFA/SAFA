<template>
  <v-expansion-panel data-cy="job-panel">
    <v-expansion-panel-header disable-icon-rotate>
      <v-row no-gutters>
        <v-col cols="4">
          <typography :value="job.name" />
        </v-col>
        <v-col cols="8">
          <v-row v-if="isCancelled(job.status)" no-gutters>
            <v-col cols="4">
              <typography secondary value="Upload Cancelled" />
            </v-col>
            <v-col cols="4">
              <typography
                secondary
                :value="getUpdatedText(job.lastUpdatedAt)"
              />
            </v-col>
          </v-row>
          <typography
            v-else-if="isCompleted(job.status)"
            secondary
            :value="getCompletedText(job.completedAt)"
          />
          <v-row v-else no-gutters>
            <v-col cols="4">
              <typography
                secondary
                :value="`Upload Progress: ${job.currentProgress}%`"
              />
            </v-col>
            <v-col cols="4">
              <typography
                secondary
                :value="getUpdatedText(job.lastUpdatedAt)"
              />
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <template v-slot:actions>
        <flex-box justify="end">
          <v-chip
            outlined
            :color="getStatusColor(job.status)"
            data-cy="job-status"
          >
            <v-progress-circular
              v-if="isInProgress(job.status)"
              :color="getStatusColor(job.status)"
              indeterminate
              size="16"
              class="mx-1"
            />
            <v-icon
              v-if="isCompleted(job.status)"
              :color="getStatusColor(job.status)"
            >
              mdi-check-circle-outline
            </v-icon>
            <v-icon
              v-if="isCancelled(job.status)"
              :color="getStatusColor(job.status)"
            >
              mdi-close-circle-outline
            </v-icon>
            <span class="ml-1">
              {{ formatStatus(job.status) }}
            </span>
          </v-chip>
        </flex-box>
      </template>
    </v-expansion-panel-header>

    <v-expansion-panel-content>
      <v-stepper alt-labels class="elevation-0" v-model="job.currentStep">
        <v-stepper-header>
          <template v-for="(step, stepIndex) in job.steps">
            <v-stepper-step :key="stepIndex" :step="stepIndex">
              <typography
                class="upload-step"
                align="center"
                el="p"
                :value="job.steps[stepIndex]"
              />
            </v-stepper-step>
            <v-divider :key="step" />
          </template>
        </v-stepper-header>
      </v-stepper>

      <flex-box full-width justify="end">
        <v-btn
          outlined
          color="error"
          class="mr-1"
          data-cy="button-delete-job"
          @click="deleteJob(job)"
        >
          Delete Upload
        </v-btn>
        <v-btn
          color="primary"
          :disabled="!isCompleted(job.status)"
          @click="viewProject(job)"
        >
          View Project
        </v-btn>
      </flex-box>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { JobModel, JobStatus } from "@/types";
import { enumToDisplay, getJobStatusColor, timestampToDisplay } from "@/util";
import { logStore } from "@/hooks";
import { handleDeleteJob, handleLoadVersion } from "@/api";
import { Typography } from "@/components/common";
import FlexBox from "@/components/common/display/FlexBox.vue";

/**
 * Displays a project import job.
 */
export default Vue.extend({
  name: "JobPanel",
  components: { FlexBox, Typography },
  props: {
    job: {
      type: Object as PropType<JobModel>,
      required: true,
    },
  },
  methods: {
    /**
     * @returns Whether the status is completed.
     */
    isCompleted(status: JobStatus) {
      return status === JobStatus.COMPLETED;
    },
    /**
     * @returns Whether the status is in progress.
     */
    isInProgress(status: JobStatus) {
      return status === JobStatus.IN_PROGRESS;
    },
    /**
     * @returns Whether the status is cancelled.
     */
    isCancelled(status: JobStatus) {
      return status === JobStatus.CANCELLED;
    },
    /**
     * @returns The display name for when this job was updated.
     */
    getUpdatedText(timestamp: string) {
      return `Last Update: ${timestampToDisplay(timestamp)}`;
    },
    /**
     * @returns The display name for when this job was completed.
     */
    getCompletedText(timestamp: string) {
      return `Upload Completed: ${timestampToDisplay(timestamp)}`;
    },
    /**
     * @returns The display name for a job status.
     */
    formatStatus(status: JobStatus): string {
      return enumToDisplay(status);
    },
    /**
     * @returns The color for a job status.
     */
    getStatusColor(status: JobStatus) {
      return getJobStatusColor(status);
    },
    /**
     * Attempts to delete a job.
     * @param job - The job to delete.
     */
    deleteJob(job: JobModel): void {
      handleDeleteJob(job, {});
    },
    /**
     * Navigates user to the completed project.
     */
    async viewProject(job: JobModel): Promise<void> {
      if (job.completedEntityId) {
        await handleLoadVersion(job.completedEntityId);
      } else {
        logStore.onError("Unable to view this project right now.");
      }
    },
  },
});
</script>

<style>
.upload-step {
  width: min-content;
}
</style>
