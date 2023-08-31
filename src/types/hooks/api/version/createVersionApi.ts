import { ComputedRef } from "vue";
import { IOHandlerCallback, VersionSchema, VersionType } from "@/types";

/**
 * A hook for calling create version API endpoints.
 */
export interface CreateVersionApiHook {
  /**
   * Whether the create version request is loading.
   */
  loading: ComputedRef<boolean>;
  /**
   * Resets the store data.
   */
  handleReset(): void;
  /**
   * Creates a new version.
   *
   * @param projectId - The project to create a version for.
   * @param versionType - The version type to create.
   * @param callbacks - The callbacks to use on success, error, and complete.
   */
  handleCreate(
    projectId: string,
    versionType: VersionType,
    callbacks: IOHandlerCallback<VersionSchema>
  ): Promise<void>;
  /**
   * Creates a new version for a project, uploading the files related to it.
   *
   * @param projectId - The project that has been selected by the user.
   * @param versionId - The version associated with given project to update.
   * @param selectedFiles  - The flat files that will update given version.
   * @param setVersionIfSuccessful - Whether the store should be set to the uploaded version if successful.
   * @param isCompleteSet - Whether to delete any other artifacts in the current version.
   */
  handleImport(
    projectId: string,
    versionId: string,
    selectedFiles: File[],
    setVersionIfSuccessful: boolean,
    isCompleteSet?: boolean
  ): Promise<void>;
}
