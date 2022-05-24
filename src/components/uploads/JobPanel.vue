<template>
  <v-expansion-panel>
    <v-expansion-panel-header disable-icon-rotate>
      <v-row no-gutters>
        <v-col cols="4">
          {{ upload.name }}
        </v-col>
        <v-col cols="8" class="text--secondary">
          <v-row v-if="isCancelled(upload.status)" no-gutters>
            <v-col cols="4"> Upload Cancelled </v-col>
            <v-col cols="4">
              {{ getUpdatedText(upload.lastUpdatedAt) }}
            </v-col>
          </v-row>
          <span v-else-if="isCompleted(upload.status)">
            {{ getCompletedText(upload.completedAt) }}
          </span>
          <v-row v-else no-gutters>
            <v-col cols="4">
              Upload Progress: {{ upload.currentProgress }}%
            </v-col>
            <v-col cols="4">
              {{ getUpdatedText(upload.lastUpdatedAt) }}
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <template v-slot:actions>
        <div style="width: 120px" class="d-flex justify-end">
          <v-chip :color="getStatusColor(upload.status)">
            <span class="mr-1">
              {{ formatStatus(upload.status) }}
            </span>
            <v-progress-circular
              v-if="isInProgress(upload.status)"
              indeterminate
              size="16"
              class="mx-1"
            />
            <v-icon v-if="isCompleted(upload.status)">
              mdi-check-circle-outline
            </v-icon>
            <v-icon v-if="isCancelled(upload.status)">
              mdi-close-circle-outline
            </v-icon>
          </v-chip>
        </div>
      </template>
    </v-expansion-panel-header>

    <v-expansion-panel-content>
      <v-stepper alt-labels class="elevation-0" v-model="upload.currentStep">
        <v-stepper-header>
          <template v-for="(step, stepIndex) in upload.steps">
            <v-stepper-step :key="stepIndex" :step="stepIndex">
              <span class="upload-step">
                {{ upload.steps[stepIndex] }}
              </span>
            </v-stepper-step>
            <v-divider :key="step" />
          </template>
        </v-stepper-header>
      </v-stepper>

      <div class="d-flex">
        <v-btn color="error" class="mr-1" @click="deleteJob(upload)">
          Delete Upload
        </v-btn>
        <v-btn color="primary" :disabled="!isCompleted(upload.status)">
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
import { handleDeleteJob } from "@/api";

/**
 * Displays a project import job.
 */
export default Vue.extend({
  name: "JobPanel",
  props: {
    upload: {
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
  },
});
</script>

<style>
.upload-step {
  width: min-content;
  text-align: center;
}
</style>
