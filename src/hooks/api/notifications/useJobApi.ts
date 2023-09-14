import { defineStore } from "pinia";

import { ref } from "vue";
import {
  ChangeMessageSchema,
  IOHandlerCallback,
  JobApiHook,
  JobLogStepSchema,
  JobSchema,
} from "@/types";
import { timestampToDisplay } from "@/util";
import { jobStore, useApi, stompApiStore } from "@/hooks";
import { deleteJobById, fillEndpoint, getJobLog, getUserJobs } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing job API requests.
 */
export const useJobApi = defineStore("jobApi", (): JobApiHook => {
  const jobApi = useApi("jobApi");

  const jobLog = ref<JobLogStepSchema[]>([]);
  const jobSteps = ref<string[]>([]);

  /**
   * Subscribes to updates for job with given id.
   *
   * @param jobId - The id for the job whose updates we want to process.
   */
  async function subscribeToJob(jobId: string): Promise<void> {
    if (!jobId) return;

    await stompApiStore.subscribeToStomp(
      fillEndpoint("jobTopic", { jobId }),
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
    await jobApi.handleRequest(async () => {
      const logs = await getJobLog(job.id);

      jobSteps.value = job.steps;
      jobLog.value = logs.map((logItems, index) => {
        const entry = logItems.map(({ entry }) => entry).join("\n\n");

        return {
          stepName: job.steps[index],
          timestamp: timestampToDisplay(
            logItems[logItems.length - 1]?.timestamp || ""
          ),
          entry,
          error: entry.includes("rror"),
        };
      });
    });
  }

  function handleCloseLogs(): void {
    jobLog.value = [];
    jobSteps.value = [];
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
        const jobs = await getUserJobs();

        for (const job of jobs) {
          await subscribeToJob(job.id);
        }

        jobStore.jobs = jobs;

        if (jobs.length === 0) return;

        jobStore.selectedJob = jobs[0];
      },
      { useAppLoad: true }
    );
  }

  return {
    jobLog,
    jobSteps,
    handleViewLogs,
    handleCloseLogs,
    handleCreate,
    handleDelete,
    handleReload,
  };
});

export default useJobApi(pinia);
