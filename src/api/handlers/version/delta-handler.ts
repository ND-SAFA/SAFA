import { EmptyLambda, ProjectDelta, VersionModel } from "@/types";
import { deltaModule, logModule } from "@/store";
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
      logModule.onSuccess("Delta state was updated successfully.");
      onComplete();
    })
    .catch((e) => {
      logModule.onError("Unable to set delta state.");
      logModule.onDevError(e.message);
    });
}
