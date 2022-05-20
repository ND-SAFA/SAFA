<template>
  <private-page>
    <template v-slot:page>
      <v-container>
        <h1 class="text-h4">Current Uploads</h1>
        <v-divider />
        <p class="text-body-1 mt-2 mb-3">
          Select a project below to see more detailed updates on the import
          status.
        </p>

        <v-expansion-panels v-model="selectedJobs" multiple>
          <template v-for="upload in uploads">
            <v-expansion-panel :key="upload.id">
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
                <v-stepper
                  alt-labels
                  class="elevation-0"
                  v-model="upload.currentStep"
                >
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
                  <v-btn
                    color="primary"
                    :disabled="!isCompleted(upload.status)"
                  >
                    View Project
                  </v-btn>
                </div>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </template>
        </v-expansion-panels>
      </v-container>
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { navigateBack } from "@/router";
import { PrivatePage } from "@/components";
import { setTimeout } from "timers";
import { connectAndSubscribeToJob, getUserJobs, handleDeleteJob } from "@/api";
import { Job, JobStatus, JobType } from "@/types";
import { jobModule } from "@/store";
import { capitalize } from "@/util";

/**
 * Displays project settings.
 */
export default Vue.extend({
  name: "UploadStatusView",
  components: {
    PrivatePage,
  },
  data() {
    return {
      timer: undefined as ReturnType<typeof setTimeout> | undefined,
      selectedJobs: [] as number[],
    };
  },
  mounted() {
    this.reloadJobs();
  },
  computed: {
    /**
     * Returns the current jobs.
     */
    uploads(): Job[] {
      return jobModule.currentJobs;
    },
    /**
     * Returns the current selected job index.
     */
    selectedJobIndex(): number {
      return jobModule.selectedJobIndex;
    },
  },
  watch: {
    /**
     * Synchronizes what jobs are selected with the selected index.
     */
    selectedJobIndex(newIndex: number): void {
      if (newIndex == -1) {
        this.selectedJobs = [];
      } else {
        this.selectedJobs = [newIndex];
      }
    },
  },
  methods: {
    /**
     * Goes back to the artifact page.
     */
    handleGoBack() {
      navigateBack();
    },
    /**
     * @return The display name for a job type.
     */
    formatJobType(jobType: JobType) {
      return capitalize(
        jobType
          .split("_")
          .map((s) => s.toLowerCase())
          .join(" ")
      );
    },
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
      return `Last Update: ${this.stringifyTimestamp(timestamp)}`;
    },
    /**
     * @returns The display name for when this job was completed.
     */
    getCompletedText(timestamp: string) {
      return `Upload Completed: ${this.stringifyTimestamp(timestamp)}`;
    },
    /**
     * // TODO: generalize
     * @returns The display name for a job status.
     */
    formatStatus(status: JobStatus): string {
      return capitalize(status.toLowerCase().split("_").join(" "));
    },
    /**
     * // TODO: generalize
     * @returns The display name for a timestamp.
     */
    stringifyTimestamp(timestamp: string) {
      const options = {
        year: "numeric",
        month: "long",
        day: "numeric",
        weekday: "long",
        hour: "numeric",
        minute: "numeric",
      };
      const date = new Date(timestamp);
      return date.toLocaleDateString("en-US", options);
    },
    /**
     * // TODO: generalize
     * @returns The color for a job status.
     */
    getStatusColor(status: JobStatus) {
      switch (status) {
        case JobStatus.COMPLETED:
          return "#64b5f6";
        case JobStatus.IN_PROGRESS:
          return "#EEBC3D";
        case JobStatus.CANCELLED:
          return "#e57373";
        default:
          return "";
      }
    },
    /**
     * Attempts to delete a job.
     * @param job - The job to delete.
     */
    deleteJob(job: Job): void {
      handleDeleteJob(job, {});
    },
    /**
     * Reloads the list of jobs.
     */
    async reloadJobs() {
      const jobs = await getUserJobs();

      for (const job of jobs) {
        await connectAndSubscribeToJob(job.id);
      }

      jobModule.SET_JOBS(jobs);
      jobModule.selectJob(jobs[jobs.length - 1]);
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
