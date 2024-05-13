import { VersionDeltaSchema } from "@/types";
import { buildRequest } from "@/api";

/**
 * Generates the delta between two project versions.
 *
 * @param sourceVersionId - The source version of the project.
 * @param targetVersionId - The target version of the project.
 * @return The delta from the source to the target versions.
 */
export async function getProjectDelta(
  targetVersionId: string,
  sourceVersionId: string
): Promise<VersionDeltaSchema> {
  return buildRequest<
    VersionDeltaSchema,
    "sourceVersionId" | "targetVersionId"
  >("delta", { sourceVersionId, targetVersionId }).get();
}
