<template>
  <v-expansion-panel data-cy="job-panel">
    <v-expansion-panel-header disable-icon-rotate>
      <v-row no-gutters>
        <v-col cols="4">
          {{ job.name }}
        </v-col>
        <v-col cols="8" class="text--secondary">
          <v-row v-if="isCancelled(job.status)" no-gutters>
            <v-col cols="4"> Upload Cancelled </v-col>
            <v-col cols="4">
              {{ getUpdatedText(job.lastUpdatedAt) }}
            </v-col>
          </v-row>
          <span v-else-if="isCompleted(job.status)">
            {{ getCompletedText(job.completedAt) }}
          </span>
          <v-row v-else no-gutters>
            <v-col cols="4">
              Upload Progress: {{ job.currentProgress }}%
            </v-col>
            <v-col cols="4">
              {{ getUpdatedText(job.lastUpdatedAt) }}
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <template v-slot:actions>
        <div style="width: 120px" class="d-flex justify-end">
          <v-chip :color="getStatusColor(job.status)" data-cy="job-status">
            <span class="mr-1">
              {{ formatStatus(job.status) }}
            </span>
            <v-progress-circular
              v-if="isInProgress(job.status)"
              indeterminate
              size="16"
              class="mx-1"
            />
            <v-icon v-if="isCompleted(job.status)">
              mdi-check-circle-outline
            </v-icon>
            <v-icon v-if="isCancelled(job.status)">
              mdi-close-circle-outline
            </v-icon>
          </v-chip>
        </div>
      </template>
    </v-expansion-panel-header>

    <v-expansion-panel-content>
      <v-stepper alt-labels class="elevation-0" v-model="job.currentStep">
        <v-stepper-header>
          <template v-for="(step, stepIndex) in job.steps">
            <v-stepper-step :key="stepIndex" :step="stepIndex">
              <span class="upload-step">
                {{ job.steps[stepIndex] }}
              </span>
            </v-stepper-step>
            <v-divider :key="step" />
          </template>
        </v-stepper-header>
      </v-stepper>

      <div class="d-flex">
        <v-btn
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
      </div>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Job, JobStatus } from "@/types";
import { enumToDisplay, getJobStatusColor, timestampToDisplay } from "@/util";
import { handleDeleteJob, handleLoadVersion } from "@/api";
import { logModule } from "@/store";

/**
 * Displays a project import job.
 * TODO: Close panel before deleting job.
 */
export default Vue.extend({
  name: "JobPanel",
  props: {
    job: {
      type: Object as PropType<Job>,
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
    deleteJob(job: Job): void {
      handleDeleteJob(job, {});
    },
    /**
     * Navigates user to the completed project.
     */
    async viewProject(job: Job): Promise<void> {
      if (job.completedEntityId) {
        await handleLoadVersion(job.completedEntityId);
      } else {
        logModule.onError("Project creation contains empty ID.");
      }
    },
  },
});
</script>

<style>
.upload-step {
  width: min-content;
  text-align: center;
}
</style>
