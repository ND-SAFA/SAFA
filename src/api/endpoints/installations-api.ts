import { InstallationSchema } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Returns the 3rd party data installations linked to a given project.
 *
 * @param projectId - The linked project.
 * @return The installations linked to this project.
 */
export async function getProjectInstallations(
  projectId: string
): Promise<InstallationSchema[]> {
  return authHttpClient<InstallationSchema[]>(
    fillEndpoint(Endpoint.getInstallations, { projectId }),
    {
      method: "GET",
    }
  );
}
