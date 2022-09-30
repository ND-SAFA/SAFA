import { IOHandlerCallback, VersionModel, VersionType } from "@/types";
import { versionToString } from "@/util";
import { logStore } from "@/hooks";
import {
  createMajorVersion,
  createMinorVersion,
  createRevisionVersion,
} from "@/api";

/**
 * Creates a new version.
 *
 * @param projectId - The project to create a version for.
 * @param versionType - The version type to create.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 * @param onComplete - Called after the action.
 */

export async function handleCreateVersion(
  projectId: string,
  versionType: VersionType,
  { onSuccess, onError, onComplete }: IOHandlerCallback<VersionModel>
): Promise<void> {
  const createVersion = () => {
    if (versionType === "major") {
      return createMajorVersion(projectId);
    } else if (versionType === "minor") {
      return createMinorVersion(projectId);
    } else {
      return createRevisionVersion(projectId);
    }
  };

  createVersion()
    .then((version) => {
      logStore.onSuccess(`Created a new version: ${versionToString(version)}`);
      onSuccess?.(version);
    })
    .catch((e) => {
      logStore.onError("Unable to create a new version.");
      onError?.(e);
    })
    .finally(onComplete);
}
