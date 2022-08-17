import { EntityChangeMessage, ProjectModel } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Get changes in EntityChangeMessage.
 * @param versionId The version of the entities to retrieve.
 * @param message The message containing set of changed entities.
 */
export async function getChanges(
  versionId: string,
  message: EntityChangeMessage
): Promise<ProjectModel> {
  return authHttpClient<ProjectModel>(
    fillEndpoint(Endpoint.sync, { versionId }),
    {
      method: "POST",
      body: JSON.stringify(message),
    }
  );
}
