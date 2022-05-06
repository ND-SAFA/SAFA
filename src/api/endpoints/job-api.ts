import { Job } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Updates an existing project from the given flat files.
 *
 * @param versionId - The project version to update.
 * @param formData - Form data containing the project files.
 * @return The updated project.
 */
export async function updateProjectThroughFlatFiles(
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
  return authHttpClient<Job[]>(
    fillEndpoint(Endpoint.getUserJobs, {}),
    {
      method: "GET",
    },
    false
  );
}
