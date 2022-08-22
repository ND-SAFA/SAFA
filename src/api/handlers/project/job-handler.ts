import { IOHandlerCallback, JobModel } from "@/types";
import {
  connect,
  deleteJobById,
  Endpoint,
  fillEndpoint,
  getUserJobs,
  stompClient,
} from "@/api";
import { appModule, jobModule } from "@/store";
import { logStore } from "@/hooks";

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

  stompClient.subscribe(fillEndpoint(Endpoint.jobTopic, { jobId }), (frame) => {
    const incomingJob: JobModel = JSON.parse(frame.body);

    jobModule.addOrUpdateJob(incomingJob);
    logStore.onDevInfo(`New Job message: ${incomingJob.id}`);
  });
}

/**
 * Subscribes to job updates via websocket messages, updates the
 * store, and selects the job.
 */
export async function handleJobSubmission(job: JobModel): Promise<void> {
  await connectAndSubscribeToJob(job.id);
  jobModule.addOrUpdateJob(job);
  jobModule.selectJob(job);
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
      jobModule.deleteJob(job);
      onSuccess?.();
    })
    .catch(onError);
}

/**
 * Reloads the current list of jobs.
 */
export async function handleReloadJobs(): Promise<void> {
  try {
    appModule.onLoadStart();

    const jobs = await getUserJobs();

    for (const job of jobs) {
      await connectAndSubscribeToJob(job.id);
    }

    jobModule.SET_JOBS(jobs);

    if (jobs.length === 0) return;

    jobModule.selectJob(jobs[0]);
  } finally {
    appModule.onLoadEnd();
  }
}
