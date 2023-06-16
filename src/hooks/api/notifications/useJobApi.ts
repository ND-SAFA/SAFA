import { defineStore } from "pinia";

import { ref } from "vue";
import {
  ChangeMessageSchema,
  IOHandlerCallback,
  JobLogSchema,
  JobSchema,
} from "@/types";
import { jobStore, useApi } from "@/hooks";
import {
  deleteJobById,
  Endpoint,
  fillEndpoint,
  getJobLog,
  getUserJobs,
} from "@/api";
import { pinia } from "@/plugins";
import stompApiStore from "./useStompApi";

export const useJobApi = defineStore("jobApi", () => {
  const jobApi = useApi("jobApi");

  const jobLog = ref<JobLogSchema[][]>([]);
  const jobSteps = ref<string[]>([]);

  /**
   * Gets the log for a job.
   * @param job - The job to view.
   */
  async function handleViewLogs(job: JobSchema): Promise<void> {
    jobLog.value = await getJobLog(job.id);
    jobSteps.value = job.steps;
  }

  /**
   * Closes the job log.
   */
  function handleCloseLogs(): void {
    jobLog.value = [];
    jobSteps.value = [];
  }

  /**
   * Subscribes to updates for job with given id.
   *
   * @param jobId - The id for the job whose updates we want to process.
   */
  async function subscribeToJob(jobId: string): Promise<void> {
    if (!jobId) return;

    await stompApiStore.subscribeToStomp(
      fillEndpoint(Endpoint.jobTopic, { jobId }),
      (frame) => {
        const job: JobSchema | ChangeMessageSchema = JSON.parse(frame.body);

        if (!("status" in job)) return;

        jobStore.updateJob(job);
      }
    );
  }

  /**
   * Subscribes to job updates via websocket messages, updates the
   * store, and selects the job.
   */
  async function handleCreate(job: JobSchema): Promise<void> {
    await subscribeToJob(job.id);
    jobStore.updateJob(job);
    jobStore.selectedJob = job;
  }

  /**
   * Deletes a job.
   *
   * @param job - The job to delete.
   * @param callbacks - The callbacks to run on success or error.
   */
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

  /**
   * Reloads the current list of jobs.
   */
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
      {},
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
