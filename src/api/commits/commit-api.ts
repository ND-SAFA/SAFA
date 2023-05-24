import { CommitSchema } from "@/types";
import { Endpoint, fillEndpoint, authHttpClient } from "@/api";

/**
 * Sends commit to backend to be saved to the database.
 *
 * @param commit The commit to be persisted to the database.
 * @return The persisted commit.
 */
export async function persistCommit(
  commit: CommitSchema
): Promise<CommitSchema> {
  const { versionId } = commit.commitVersion;

  return authHttpClient<CommitSchema>(
    fillEndpoint(Endpoint.commit, { versionId }),
    {
      method: "POST",
      body: JSON.stringify(commit),
    }
  );
}
