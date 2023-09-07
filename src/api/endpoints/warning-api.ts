import { WarningCollectionSchema } from "@/types";
import { buildRequest } from "@/api";

/**
 * Returns the project warnings in the given project version.
 *
 * @param versionId The version id whose warnings are returned.
 * @return The project warnings.
 */
export async function getWarningsInProjectVersion(
  versionId: string
): Promise<WarningCollectionSchema> {
  return buildRequest<WarningCollectionSchema, "versionId">(
    "getWarningsInProjectVersion"
  )
    .withParam("versionId", versionId)
    .get();
}
