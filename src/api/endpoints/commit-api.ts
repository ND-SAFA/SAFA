import { CommitSchema } from "@/types";
import { buildRequest } from "@/api";

/**
 * Sends commit to backend to be saved to the database.
 *
 * @param commit The commit to be persisted to the database.
 * @return The persisted commit.
 */
export async function persistCommit(
  commit: CommitSchema
): Promise<CommitSchema> {
  return buildRequest<CommitSchema, "versionId", CommitSchema>("commit", {
    versionId: commit.commitVersion.versionId,
  }).post(commit);
}
