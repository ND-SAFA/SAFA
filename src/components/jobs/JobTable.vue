<template>
  <v-data-table
    single-expand
    show-expand
    :headers="headers"
    :items="jobs"
    :expanded="expanded"
    :loading="isLoading"
    data-cy="job-table"
    @click:row="handleView($event)"
  >
    <template v-slot:[`item.name`]="{ item }">
      <typography bold :value="item.name" />
    </template>
    <template v-slot:[`item.currentProgress`]="{ item }">
      <v-row v-if="isCancelled(item.status)" no-gutters>
        <v-col cols="4">
          <typography secondary value="Upload Cancelled" />
        </v-col>
        <v-col cols="4">
          <typography secondary :value="getUpdatedText(item.lastUpdatedAt)" />
        </v-col>
      </v-row>
      <typography
        v-else-if="isCompleted(item.status)"
        secondary
        :value="getCompletedText(item.completedAt)"
      />
      <v-row v-else no-gutters>
        <v-col cols="4">
          <typography
            secondary
            :value="`Upload Progress: ${item.currentProgress}%`"
          />
        </v-col>
        <v-col cols="4">
          <typography secondary :value="getUpdatedText(item.lastUpdatedAt)" />
        </v-col>
      </v-row>
    </template>
    <template v-slot:[`item.status`]="{ item }">
      <v-chip
        outlined
        :color="getStatusColor(item.status)"
        data-cy="job-status"
      >
        <v-progress-circular
          v-if="isInProgress(item.status)"
          :color="getStatusColor(item.status)"
          indeterminate
          size="16"
          class="mx-1"
        />
        <v-icon
          v-if="isCompleted(item.status)"
          :color="getStatusColor(item.status)"
        >
          mdi-check-circle-outline
        </v-icon>
        <v-icon
          v-if="isCancelled(item.status)"
          :color="getStatusColor(item.status)"
        >
          mdi-close-circle-outline
        </v-icon>
        <span class="ml-1">
          {{ formatStatus(item.status) }}
        </span>
      </v-chip>
    </template>
    <template v-slot:expanded-item="{ headers, item }">
      <td :colspan="headers.length">
        <v-container>
          <v-stepper alt-labels class="elevation-0" v-model="item.currentStep">
            <v-stepper-header>
              <template v-for="(step, stepIndex) in item.steps">
                <v-stepper-step :key="stepIndex" :step="stepIndex">
                  <typography
                    class="upload-step"
                    align="center"
                    el="p"
                    :value="item.steps[stepIndex]"
                  />
                </v-stepper-step>
                <v-divider
                  :key="step"
                  v-if="stepIndex < item.steps.length - 1"
                />
              </template>
            </v-stepper-header>
          </v-stepper>

          <flex-box full-width justify="end">
            <v-btn
              outlined
              color="error"
              class="mr-1"
              data-cy="button-delete-job"
              @click="handleDeleteJob(item)"
            >
              Delete Upload
            </v-btn>
            <v-btn
              color="primary"
              :disabled="!isCompleted(item.status)"
              data-cy="button-open-job"
              @click="handleViewProject(item)"
            >
              View Project
            </v-btn>
          </flex-box>
        </v-container>
      </td>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import Vue from "vue";
import { JobModel, JobStatus } from "@/types";
import { enumToDisplay, getJobStatusColor, timestampToDisplay } from "@/util";
import { appStore, jobStore, logStore } from "@/hooks";
import { handleDeleteJob, handleLoadVersion, handleReloadJobs } from "@/api";
import { Typography, FlexBox } from "@/components/common";

/**
 * Renders a list of jobs.
 */
export default Vue.extend({
  name: "JobTable",
  components: { Typography, FlexBox },
  props: {},
  data() {
    return {
      headers: [
        { text: "Name", value: "name" },
        { text: "Progress", value: "currentProgress" },
        { text: "Status", value: "status" },
      ],
      expanded: [] as JobModel[],
    };
  },
  mounted() {
    this.handleRefresh();
  },
  computed: {
    /**
     * @return Whether the app is loading.
     */
    isLoading(): boolean {
      return appStore.isLoading > 0;
    },
    /**
     * return The current jobs.
     */
    jobs(): JobModel[] {
      return jobStore.jobs;
    },
    /**
     * return The current selected job index.
     */
    selectedJobIndex(): number {
      return jobStore.selectedJob;
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
    formatStatus(status?: JobStatus): string {
      return enumToDisplay(status || "");
    },
    /**
     * @returns The color for a job status.
     */
    getStatusColor(status?: JobStatus): string {
      return status ? getJobStatusColor(status) : "";
    },
    /**
     * Reloads the list of jobs.
     */
    async handleRefresh() {
      await handleReloadJobs();
    },
    /**
     * Opens the view job expansion panel.
     * @param job - The job to view.
     */
    handleView(job: JobModel): void {
      if (job === this.expanded[0]) {
        this.expanded = [];
      } else {
        this.expanded = [job];
      }
    },
    /**
     * Attempts to delete a job.
     * @param job - The job to delete.
     */
    handleDeleteJob(job: JobModel): void {
      handleDeleteJob(job, {});
    },
    /**
     * Navigates user to the completed project.
     */
    async handleViewProject(job: JobModel): Promise<void> {
      if (job.completedEntityId) {
        await handleLoadVersion(job.completedEntityId);
      } else {
        logStore.onError("Unable to view this project right now.");
      }
    },
  },
  watch: {
    /**
     * Synchronizes what jobs are selected with the selected index.
     */
    selectedJobIndex(newIndex: number): void {
      if (newIndex == -1) {
        this.expanded = [];
      } else {
        this.expanded = [this.jobs[newIndex]];
      }
    },
  },
});
</script>
