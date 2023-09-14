import { Ref } from "vue";
import { IOHandlerCallback, JobLogStepSchema, JobSchema } from "@/types";

/**
 * A hook for calling job API endpoints.
 */
export interface JobApiHook {
  /**
   * Logs for the current job.
   */
  jobLog: Ref<JobLogStepSchema[]>;
  /**
   * Gets the log for a job.
   *
   * @param job - The job to view.
   */
  handleViewLogs(job: JobSchema): Promise<void>;
  /**
   * Closes the job log.
   */
  handleCloseLogs(): void;
  /**
   * Downloads the viewed job logs as a markdown file.
   */
  handleDownloadLogs(): void;
  /**
   * Subscribes to job updates via websocket messages, updates the
   * store, and selects the job.
   *
   * @param job - The job to create.
   */
  handleCreate(job: JobSchema): Promise<void>;
  /**
   * Deletes a job.
   *
   * @param job - The job to delete.
   * @param callbacks - The callbacks to run on success or error.
   */
  handleDelete(job: JobSchema, callbacks: IOHandlerCallback): Promise<void>;
  /**
   * Reloads the current list of jobs.
   */
  handleReload(): Promise<void>;
}
