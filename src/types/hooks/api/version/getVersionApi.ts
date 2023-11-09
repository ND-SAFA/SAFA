import { ComputedRef, Ref, WritableComputedRef } from "vue";
import {
  DocumentSchema,
  IdentifierSchema,
  IOHandlerCallback,
  VersionSchema,
} from "@/types";

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
   * All versions for the currently loaded project.
   */
  allVersions: Ref<VersionSchema[]>;
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
  handleReload(
    projectId?: string,
    callbacks?: IOHandlerCallback<VersionSchema[]>
  ): Promise<void>;
  /**
   * Load the given project version.
   * Navigates to the artifact view page to show the loaded project.
   *
   * @param versionId - The id of the version to retrieve and load.
   * @param document - The document to start with viewing.
   * @param doNavigate - Whether to navigate to the artifact tree if not already on an artifact page.
   *        @default true
   */
  handleLoad(
    versionId: string,
    document?: DocumentSchema,
    doNavigate?: boolean
  ): Promise<void>;
  /**
   * Load the current version of the given project.
   *
   * @param identifier - The project to load the current version of.
   */
  handleLoadCurrent(
    identifier: Pick<IdentifierSchema, "projectId">
  ): Promise<void>;
}
