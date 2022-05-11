import { Job } from "@/types";
import { connectAndSubscribeToJob, submitFlatFileUploadJob } from "@/api";
import { jobModule } from "@/store";

/**
 * Submits new job to upload flat files to project version with given id.
 * Then, subscribes to job updates via websocket messages which update the
 * store.
 * @param versionId The project version to commit entities from flat files to.
 * @param formData The data containing the flat files.
 */
export async function handleJobSubmission(
  versionId: string,
  formData: FormData
): Promise<Job> {
  const job = await submitFlatFileUploadJob(versionId, formData);
  await connectAndSubscribeToJob(job.id);
  jobModule.addOrUpdateJob(job);
  jobModule.selectJob(job);
  return job;
}
