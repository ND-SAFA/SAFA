import { ComputedRef, WritableComputedRef } from "vue";
import { IdentifierSchema, IOHandlerCallback, VersionSchema } from "@/types";

/**
 * A hook for calling get version API endpoints.
 */
export interface GetVersionApiHook {
  /**
   * Whether the get versions request is loading.
   */
  getLoading: ComputedRef<boolean>;
  /**
   * Whether the load version request is loading.
   */
  loadLoading: ComputedRef<boolean>;
  /**
   * Whether the delete version request is loading.
   */
  deleteLoading: ComputedRef<boolean>;
  /**
   * The current loaded project.
   * - Reactively loads the current project when set.
   */
  currentProject: WritableComputedRef<IdentifierSchema | undefined>;
  /**
   * The currently loaded project version.
   * - Reactively loads a new project version when updated.
   */
  currentVersion: WritableComputedRef<VersionSchema | undefined>;
  /**
   * Loads the versions of a project.
   * If no project id is given, the current project is used, and all versions will be set.
   *
   * @param projectId - The id of the project to load the versions of.
   * @param callbacks - Callbacks for the action.
   */
  handleLoadVersions(
    projectId?: string,
    callbacks?: IOHandlerCallback<VersionSchema[]>
  ): Promise<void>;
  /**
   * Load the given project version.
   * Navigates to the artifact view page to show the loaded project.
   *
   * @param versionId - The ID of the version to retrieve and load.
   * @param viewId - The ID of an artifact or document to navigate to after loading the version.
   * @param doNavigate - Whether to navigate to the artifact tree if not already on an artifact page.
   *        @default true
   * @param callbacks - Callbacks for the action.
   */
  handleLoad(
    versionId: string,
    viewId?: string,
    doNavigate?: boolean,
    callbacks?: IOHandlerCallback
  ): Promise<void>;
  /**
   * Load the current version of the given project.
   *
   * @param identifier - The project to load the current version of.
   * @param callbacks - Callbacks for the action.
   */
  handleLoadCurrent(
    identifier: Pick<IdentifierSchema, "projectId">,
    callbacks?: IOHandlerCallback
  ): Promise<void>;
  /**
   * Deletes a version, updates app state, and logs the status.
   *
   * @param version - The version to delete.
   * @param callbacks - Callbacks for the action.
   */
  handleDelete(version: VersionSchema, callbacks?: IOHandlerCallback): void;
}
