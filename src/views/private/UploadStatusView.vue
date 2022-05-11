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
                    Delete Job
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
import { connectAndSubscribeToJob, deleteJobById, getUserJobs } from "@/api";
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
    uploads(): Job[] {
      return jobModule.jobs;
    },
    selectedJobIndex(): number {
      // allows us to watch it below
      return jobModule.selectedJob;
    },
  },
  watch: {
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
    formatJobType(jobType: JobType) {
      return capitalize(
        jobType
          .split("_")
          .map((s) => s.toLowerCase())
          .join(" ")
      );
    },
    isCompleted(status: JobStatus) {
      return status === JobStatus.COMPLETED;
    },
    isInProgress(status: JobStatus) {
      return status === JobStatus.IN_PROGRESS;
    },
    isCancelled(status: JobStatus) {
      return status === JobStatus.CANCELLED;
    },
    getUpdatedText(timestamp: string) {
      return `Last Update: ${this.stringifyTimestamp(timestamp)}`;
    },
    getCompletedText(timestamp: string) {
      return `Upload Completed: ${this.stringifyTimestamp(timestamp)}`;
    },
    formatStatus(status: JobStatus): string {
      return capitalize(status.toLowerCase().split("_").join(" "));
    },
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
    async deleteJob(job: Job): Promise<void> {
      await deleteJobById(job.id);
      jobModule.deleteJob(job);
    },
    async reloadJobs() {
      const jobs = await getUserJobs();
      let currentJob = jobs[0];
      jobModule.SET_JOBS(jobs);
      for (const job of jobs) {
        await connectAndSubscribeToJob(job.id);
        currentJob = job;
      }
      jobModule.selectJob(currentJob);
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
