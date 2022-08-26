import { IOHandlerCallback, JobModel } from "@/types";
import { appStore, jobStore } from "@/hooks";
import { connect, deleteJobById, Endpoint, fillEndpoint, getUserJobs, stompClient } from "@/api";
import { Frame } from "webstomp-client";

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
 * @param frame The frame to be
 */
export async function updateJobFromWebsocketMessage(frame: Frame) {
  const job: JobModel = JSON.parse(frame.body);
  jobStore.updateJob(job);
}

/**
 * Subscribes to job updates via websocket messages, updates the
 * store, and selects the job.
 */
export async function handleJobSubmission(job: JobModel): Promise<void> {
  await connectAndSubscribeToJob(job.id);
  jobStore.updateJob(job);
  jobStore.selectJob(job);
}

/**
 * Deletes a job.
 *
 * @param job - The job to delete.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleDeleteJob(
  job: JobModel,
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

    jobStore.$patch({ jobs });

    if (jobs.length === 0) return;

    jobStore.selectJob(jobs[0]);
  } finally {
    appStore.onLoadEnd();
  }
}
