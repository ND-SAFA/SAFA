import { Commit } from "@/types";
import { Endpoint, fillEndpoint, authHttpClient } from "@/api/util";

/**
 * Sends commit to backend to be saved to the database.
 *
 * @param commit The commit to be persisted to the database.
 */
export async function persistCommit(commit: Commit): Promise<Commit> {
  const { versionId } = commit.commitVersion;

  return authHttpClient<Commit>(fillEndpoint(Endpoint.commit, { versionId }), {
    method: "POST",
    body: JSON.stringify(commit),
  });
}
