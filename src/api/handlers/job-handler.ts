import { IOHandlerCallback, Job } from "@/types";
import {
  connectAndSubscribeToJob,
  createFlatFileUploadJob,
  deleteJobById,
} from "@/api";
import { jobModule } from "@/store";

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
