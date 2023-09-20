import { ChangeMessageSchema, ProjectSchema } from "@/types";
import { buildRequest } from "@/api";

/**
 * Get changes in EntityChangeMessage.
 *
 * @param versionId - The version of the entities to retrieve.
 * @param message - The message containing set of changed entities.
 * @return A project object with reflected changes.
 */
export async function getChanges(
  versionId: string,
  message: ChangeMessageSchema
): Promise<ProjectSchema> {
  return buildRequest<ProjectSchema, "versionId", ChangeMessageSchema>("sync", {
    versionId,
  }).post(message);
}
