import { NameValidationSchema } from "@/types";
import { Endpoint, fillEndpoint, authHttpClient } from "@/api";

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
  const res = await authHttpClient<NameValidationSchema>(
    fillEndpoint(Endpoint.isArtifactNameTaken, { versionId }),
    { method: "POST", body: JSON.stringify({ artifactName }) }
  );

  return res.artifactExists;
}
