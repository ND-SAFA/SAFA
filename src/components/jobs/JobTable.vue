<template>
  <panel-card>
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
      <template #[`item.name`]="{ item }">
        <typography bold :value="item.name" />
      </template>
      <template #[`item.currentProgress`]="{ item }">
        <v-row v-if="isCancelled(item.status)" no-gutters>
          <v-col cols="4">
            <typography secondary value="Cancelled" />
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
              data-cy="job-progress"
            />
          </v-col>
          <v-col cols="4">
            <typography secondary :value="getUpdatedText(item.lastUpdatedAt)" />
          </v-col>
        </v-row>
      </template>
      <template #[`item.status`]="{ item }">
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
      <template #expanded-item="{ headers, item }">
        <td :colspan="headers.length">
          <v-container>
            <v-stepper
              v-model="item.currentStep"
              alt-labels
              class="elevation-0"
              style="background-color: transparent"
            >
              <v-stepper-header>
                <template
                  v-for="(step, stepIndex) in item.steps"
                  :key="stepIndex"
                >
                  <v-stepper-step :step="stepIndex">
                    <typography
                      class="upload-step"
                      align="center"
                      el="p"
                      :value="item.steps[stepIndex]"
                    />
                  </v-stepper-step>
                  <v-divider
                    v-if="stepIndex < item.steps.length - 1"
                    :key="step"
                  />
                </template>
              </v-stepper-header>
            </v-stepper>

            <flex-box full-width justify="end">
              <text-button
                outlined
                class="mr-1"
                data-cy="button-job-log"
                icon-id="mdi-post-outline"
                @click="handleViewLogs(item)"
              >
                View Logs
              </text-button>
              <text-button
                outlined
                variant="delete"
                class="mr-1"
                data-cy="button-delete-job"
                @click="handleDeleteJob(item)"
              >
                Delete Upload
              </text-button>
              <text-button
                color="primary"
                :disabled="!isCompleted(item.status)"
                data-cy="button-open-job"
                icon-id="mdi-family-tree"
                @click="handleViewProject(item)"
              >
                View Project
              </text-button>
            </flex-box>
          </v-container>
        </td>
      </template>
    </v-data-table>
    <modal
      title="Logs"
      :is-open="jobLog.length > 0"
      :actions-height="0"
      @close="handleCloseLogs"
    >
      <template #body>
        <typography
          t="4"
          default-expanded
          variant="code"
          :value="log"
          data-cy="text-job-log"
        />
      </template>
    </modal>
  </panel-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { JobLogSchema, JobSchema, JobStatus } from "@/types";
import { enumToDisplay, getJobStatusColor, timestampToDisplay } from "@/util";
import { appStore, jobStore, logStore } from "@/hooks";
import {
  getJobLog,
  handleDeleteJob,
  handleLoadVersion,
  handleReloadJobs,
} from "@/api";
import { Typography, FlexBox, PanelCard, Modal } from "@/components/common";
import TextButton from "@/components/common/button/TextButton.vue";

/**
 * Renders a list of jobs.
 */
export default defineComponent({
  name: "JobTable",
  components: { TextButton, Modal, PanelCard, Typography, FlexBox },
  props: {},
  data() {
    return {
      headers: [
        { text: "Name", value: "name" },
        { text: "Progress", value: "currentProgress" },
        { text: "Status", value: "status" },
      ],
      jobLog: [] as JobLogSchema[],
    };
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
    jobs(): JobSchema[] {
      return jobStore.jobs;
    },
    /**
     * return The current selected job index.
     */
    expanded(): JobSchema[] {
      return jobStore.selectedJob ? [jobStore.selectedJob] : [];
    },
    /**
     * return The current selected job index.
     */
    log(): string {
      return JSON.stringify(this.jobLog, null, 2);
    },
  },
  mounted() {
    this.handleRefresh();
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
      return `Updated: ${timestampToDisplay(timestamp)}`;
    },
    /**
     * @returns The display name for when this job was completed.
     */
    getCompletedText(timestamp: string) {
      return `Completed: ${timestampToDisplay(timestamp)}`;
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
    handleView(job: JobSchema): void {
      jobStore.selectedJob = job;
    },
    /**
     * Attempts to delete a job.
     * @param job - The job to delete.
     */
    handleDeleteJob(job: JobSchema): void {
      handleDeleteJob(job, {});
    },
    /**
     * Navigates user to the completed project.
     */
    async handleViewProject(job: JobSchema): Promise<void> {
      if (job.completedEntityId) {
        await handleLoadVersion(job.completedEntityId);
      } else {
        logStore.onError("Unable to view this project right now.");
      }
    },
    /**
     * Gets the log for a job.
     * @param job - The job to view.
     */
    async handleViewLogs(job: JobSchema): Promise<void> {
      this.jobLog = await getJobLog(job.id);
    },
    /**
     * Closes the job log.
     */
    handleCloseLogs(): void {
      this.jobLog = [];
    },
  },
});
</script>
