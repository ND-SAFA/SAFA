import { EmptyLambda, ProjectDelta, VersionModel } from "@/types";
import { deltaModule } from "@/store";
import { logStore } from "@/hooks";
import { getProjectDelta } from "@/api";

/**
 * Sets a project delta.
 *
 * @param sourceVersion - The source version of the project.
 * @param targetVersion - The target version of the project.
 * @param onComplete - Ran if the operation is successful.
 */
export function handleSetProjectDelta(
  sourceVersion: VersionModel,
  targetVersion: VersionModel,
  onComplete: EmptyLambda
): void {
  getProjectDelta(sourceVersion.versionId, targetVersion.versionId)
    .then(async (deltaPayload: ProjectDelta) => {
      await deltaModule.setDeltaPayload(deltaPayload);
      deltaModule.setAfterVersion(targetVersion);
      logStore.onSuccess("Delta state was updated successfully.");
      onComplete();
    })
    .catch((e) => {
      logStore.onError("Unable to set delta state.");
      logStore.onDevError(e.message);
    });
}
