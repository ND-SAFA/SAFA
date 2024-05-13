import { defineStore } from "pinia";

import { ref } from "vue";
import { saveAs } from "file-saver";
import {
  ChangeMessageSchema,
  IOHandlerCallback,
  JobApiHook,
  JobLogStepSchema,
  JobSchema,
} from "@/types";
import { timestampToDisplay } from "@/util";
import { jobStore, projectStore, stompApiStore, useApi } from "@/hooks";
import {
  deleteJobById,
  fillEndpoint,
  getJobLog,
  getProjectJobs,
  getUserJobs,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing job API requests.
 */
export const useJobApi = defineStore("jobApi", (): JobApiHook => {
  const jobApi = useApi("jobApi");

  const jobLog = ref<JobLogStepSchema[]>([]);
  const viewedJob = ref<JobSchema | undefined>();

  /**
   * Subscribes to updates for job with given id.
   *
   * @param jobId - The id for the job whose updates we want to process.
   */
  async function subscribeToJob(jobId: string): Promise<void> {
    if (!jobId) return;

    await stompApiStore.subscribeTo(
      fillEndpoint("topicJobs", { jobId }),
      async (frame) => {
        await jobApi.handleRequest(async () => {
          const job: JobSchema | ChangeMessageSchema = JSON.parse(frame.body);

          if (!("status" in job)) return;

          jobStore.updateJob(job);
        });
      }
    );
  }

  async function handleViewLogs(job: JobSchema): Promise<void> {
    viewedJob.value = job;
    jobStore.selectedJob = job;

    await jobApi.handleRequest(async () => {
      const logs = await getJobLog(job.id);

      jobLog.value = logs
        .map((logItems, index) => {
          const entry = logItems.map(({ entry }) => entry).join("\n\n");
          const isoTimestamp = logItems[logItems.length - 1]?.timestamp;

          return {
            stepName: job.steps[index],
            timestamp: isoTimestamp ? timestampToDisplay(isoTimestamp) : "",
            entry,
            error: entry.includes("Error executing job"),
          };
        })
        .filter(({ entry }) => !!entry);
    });
  }

  function handleCloseLogs(): void {
    jobLog.value = [];
    viewedJob.value = undefined;
  }

  function handleDownloadLogs(): void {
    if (!viewedJob.value) return;

    const fileName = `${viewedJob.value.name}-${viewedJob.value.lastUpdatedAt}.md`;
    const blob = new Blob(
      jobLog.value.map(
        (step) => `# ${step.stepName}\n\n${step.timestamp}\n\n${step.entry}`
      ),
      { type: "text/plain;charset=utf-8" }
    );

    saveAs(blob, fileName);
  }

  async function handleCreate(job: JobSchema): Promise<void> {
    await subscribeToJob(job.id);
    jobStore.updateJob(job);
    jobStore.selectedJob = job;
  }

  async function handleDelete(
    job: JobSchema,
    callbacks: IOHandlerCallback
  ): Promise<void> {
    await jobApi.handleRequest(() => deleteJobById(job.id), {
      ...callbacks,
      onSuccess: () => {
        jobStore.deleteJob(job);
        callbacks.onSuccess?.();
      },
    });
  }

  async function handleReload(): Promise<void> {
    await jobApi.handleRequest(
      async () => {
        if (projectStore.projectId) {
          jobStore.projectJobs = await getProjectJobs(projectStore.projectId);
        }

        const userJobs = await getUserJobs();

        for (const job of userJobs) {
          if (job.status !== "IN_PROGRESS") continue;
          await subscribeToJob(job.id);
        }

        jobStore.jobs = userJobs;

        if (userJobs.length === 0) return;

        jobStore.selectedJob = userJobs[0];
      },
      { useAppLoad: true }
    );
  }

  return {
    jobLog,
    handleViewLogs,
    handleCloseLogs,
    handleDownloadLogs,
    handleCreate,
    handleDelete,
    handleReload,
  };
});

export default useJobApi(pinia);
