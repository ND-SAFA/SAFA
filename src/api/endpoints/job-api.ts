import { JobLogSchema, JobSchema } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

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
  return authHttpClient<JobSchema>(
    fillEndpoint(Endpoint.updateProjectThroughFlatFiles, { versionId }),
    {
      method: "POST",
      body: formData,
    },
    { setJsonContentType: false }
  );
}

/**
 * Returns list of jobs created by user.
 *
 * @return Uses list.
 */
export async function getUserJobs(): Promise<JobSchema[]> {
  return authHttpClient<JobSchema[]>(fillEndpoint(Endpoint.getUserJobs, {}), {
    method: "GET",
  });
}

/**
 * Deletes the job with given id.
 *
 * @param jobId - The job to delete.
 */
export async function deleteJobById(jobId: string): Promise<void> {
  return authHttpClient<void>(fillEndpoint(Endpoint.deleteJobById, { jobId }), {
    method: "DELETE",
  });
}

/**
 * Returns the logs for a job.
 *
 * @param jobId - The job to get logs for.
 */
export async function getJobLog(jobId: string): Promise<JobLogSchema[]> {
  return authHttpClient<JobLogSchema[]>(
    fillEndpoint(Endpoint.getJobLog, { jobId }),
    {
      method: "GET",
    }
  );
}
