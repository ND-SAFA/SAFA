import { ChangeMessageModel, ProjectModel } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Get changes in EntityChangeMessage.
 *
 * @param versionId - The version of the entities to retrieve.
 * @param message - The message containing set of changed entities.
 * @return A project object with reflected changes.
 */
export async function getChanges(
  versionId: string,
  message: ChangeMessageModel
): Promise<ProjectModel> {
  return authHttpClient<ProjectModel>(
    fillEndpoint(Endpoint.sync, { versionId }),
    {
      method: "POST",
      body: JSON.stringify(message),
    }
  );
}
