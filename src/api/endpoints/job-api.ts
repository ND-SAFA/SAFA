import { JobLogSchema, JobSchema } from "@/types";
import { buildRequest } from "@/api";

/**
 * Creates a project from the given flat files.
 *
 * @param formData - Form data containing the project files.
 * @return The created project.
 */
export async function createProjectUploadJob(
  formData: FormData
): Promise<JobSchema> {
  //TODO: include org, team
  return buildRequest<JobSchema, string, FormData>(
    "createProjectThroughFlatFiles"
  )
    .withFormData()
    .post(formData);
}

/**
 * Updates an existing project from the given flat files.
 *
 * @param versionId - The project version to update.
 * @param formData - Form data containing the project files.
 * @return The updated project.
 */
export async function createFlatFileUploadJob(
  versionId: string,
  formData: FormData
): Promise<JobSchema> {
  return buildRequest<JobSchema, "versionId", FormData>(
    "updateProjectThroughFlatFiles"
  )
    .withParam("versionId", versionId)
    .withFormData()
    .post(formData);
}

/**
 * Returns list of jobs created by user.
 *
 * @return Uses list.
 */
export async function getUserJobs(): Promise<JobSchema[]> {
  return buildRequest<JobSchema[]>("getUserJobs").get();
}

/**
 * Deletes the job with given id.
 *
 * @param jobId - The job to delete.
 */
export async function deleteJobById(jobId: string): Promise<void> {
  return buildRequest<void, "jobId">("deleteJobById")
    .withParam("jobId", jobId)
    .delete();
}

/**
 * Returns the logs for a job.
 *
 * @param jobId - The job to get logs for.
 */
export async function getJobLog(jobId: string): Promise<JobLogSchema[][]> {
  return buildRequest<JobLogSchema[][], "jobId">("getJobLog")
    .withParam("jobId", jobId)
    .get();
}
