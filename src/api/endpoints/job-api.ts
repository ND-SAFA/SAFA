import { Job } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Updates an existing project from the given flat files.
 *
 * @param versionId - The project version to update.
 * @param formData - Form data containing the project files.
 * @return The updated project.
 */
export async function submitFlatFileUploadJob(
  versionId: string,
  formData: FormData
): Promise<Job> {
  return authHttpClient<Job>(
    fillEndpoint(Endpoint.updateProjectThroughFlatFiles, { versionId }),
    {
      method: "POST",
      body: formData,
    },
    false
  );
}

/**
 * Returns list of jobs created by user.
 */
export async function getUserJobs(): Promise<Job[]> {
  return authHttpClient<Job[]>(fillEndpoint(Endpoint.getUserJobs, {}), {
    method: "GET",
  });
}

/**
 * Deletes job with given id
 */
export async function deleteJobById(jobId: string): Promise<void> {
  return authHttpClient<void>(fillEndpoint(Endpoint.deleteJobById, { jobId }), {
    method: "DELETE",
  });
}
