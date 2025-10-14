import {
  NameValidationRequestSchema,
  NameValidationResponseSchema,
} from "@/types";
import { buildRequest } from "@/api";

/**
 * Returns whether the given artifact name already exists.
 *
 * @param versionId - The project version to search within.
 * @param artifactName - The artifact name to search for.
 * @return Whether the artifact name is already taken.
 */
export async function getDoesArtifactExist(
  versionId: string,
  artifactName: string
): Promise<boolean> {
  return (
    await buildRequest<
      NameValidationResponseSchema,
      "versionId",
      NameValidationRequestSchema
    >("isArtifactNameTaken", { versionId }).post({ artifactName })
  ).artifactExists;
}
