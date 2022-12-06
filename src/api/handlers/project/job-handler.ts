import { Frame } from "webstomp-client";
import { ChangeMessageSchema, IOHandlerCallback, JobSchema } from "@/types";
import { appStore, jobStore } from "@/hooks";
import {
  connect,
  deleteJobById,
  Endpoint,
  fillEndpoint,
  getUserJobs,
  stompClient,
} from "@/api";

/**
 * Subscribes to updates for job with given id.
 *
 * @param jobId - The id for the job whose updates we want to process.
 */
export async function connectAndSubscribeToJob(jobId: string): Promise<void> {
  if (!jobId) {
    return;
  }

  await connect();

  stompClient.subscribe(
    fillEndpoint(Endpoint.jobTopic, { jobId }),
    updateJobFromWebsocketMessage
  );
}

/**
 * Extracts job from websocket message and updates the according job.
 * @param frame - The websocket frame including job update message.
 */
export function updateJobFromWebsocketMessage(frame: Frame): void {
  const job: JobSchema | ChangeMessageSchema = JSON.parse(frame.body);

  if (!("jobType" in job)) return;

  jobStore.updateJob(job);
}

/**
 * Subscribes to job updates via websocket messages, updates the
 * store, and selects the job.
 */
export async function handleJobSubmission(job: JobSchema): Promise<void> {
  await connectAndSubscribeToJob(job.id);
  jobStore.updateJob(job);
  jobStore.selectedJob = job;
}

/**
 * Deletes a job.
 *
 * @param job - The job to delete.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleDeleteJob(
  job: JobSchema,
  { onSuccess, onError }: IOHandlerCallback
): void {
  deleteJobById(job.id)
    .then(() => {
      jobStore.deleteJob(job);
      onSuccess?.();
    })
    .catch(onError);
}

/**
 * Reloads the current list of jobs.
 */
export async function handleReloadJobs(): Promise<void> {
  try {
    appStore.onLoadStart();

    const jobs = await getUserJobs();

    for (const job of jobs) {
      await connectAndSubscribeToJob(job.id);
    }

    jobStore.jobs = jobs;

    if (jobs.length === 0) return;

    jobStore.selectedJob = jobs[0];
  } finally {
    appStore.onLoadEnd();
  }
}
