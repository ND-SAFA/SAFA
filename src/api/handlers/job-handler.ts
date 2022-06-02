import { IOHandlerCallback, Job } from "@/types";
import {
  connect,
  createFlatFileUploadJob,
  deleteJobById,
  Endpoint,
  fillEndpoint,
  stompClient,
} from "@/api";
import { jobModule, logModule } from "@/store";

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
    const incomingJob: Job = JSON.parse(frame.body);

    jobModule.addOrUpdateJob(incomingJob);
    logModule.onDevMessage(`New Job message: ${incomingJob.id}`);
  });
}

/**
 * Submits new job to upload flat files to project version with given id.
 * Then, subscribes to job updates via websocket messages which update the
 * store.
 *
 * @param versionId - The project version to commit entities from flat files to.
 * @param formData - The data containing the flat files.
 * @return The created job.
 */
export async function handleJobSubmission(
  versionId: string,
  formData: FormData
): Promise<Job> {
  const job = await createFlatFileUploadJob(versionId, formData);

  await connectAndSubscribeToJob(job.id);
  jobModule.addOrUpdateJob(job);
  jobModule.selectJob(job);

  return job;
}

/**
 * Deletes a job.
 *
 * @param job - The job to delete.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
export function handleDeleteJob(
  job: Job,
  { onSuccess, onError }: IOHandlerCallback
): void {
  deleteJobById(job.id)
    .then(() => {
      jobModule.deleteJob(job);
      onSuccess?.();
    })
    .catch(onError);
}
