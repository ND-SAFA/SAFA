import { ComputedRef } from "vue";
import { IOHandlerCallback, ProjectSchema, VersionSchema } from "@/types";

/**
 * A hook for calling project API endpoints.
 */
export interface ProjectApiHook {
  /**
   * Whether the save project request is loading.
   */
  saveProjectLoading: ComputedRef<boolean>;
  /**
   * Whether the delete project request is loading.
   */
  deleteProjectLoading: ComputedRef<boolean>;
  /**
   * Whether the delete version request is loading.
   */
  deleteVersionLoading: ComputedRef<boolean>;
  /**
   * Saves a project, updates app state, and logs the status.
   *
   * @param callbacks - Callbacks for the action.
   */
  handleSave(callbacks?: IOHandlerCallback<ProjectSchema>): Promise<void>;
  /**
   * Creates a file download for project files, either in csv for json format.
   *
   * @param fileType - The file format to download.
   *        @default 'csv'
   */
  handleDownload(fileType?: "csv" | "json"): Promise<void>;
  /**
   * Deletes a project, updates app state, and logs the status.
   *
   * @param callbacks - Callbacks for the action.
   */
  handleDeleteProject(callbacks: IOHandlerCallback): Promise<void>;
  /**
   * Deletes a version, updates app state, and logs the status.
   *
   * @param version - The version to delete.
   * @param callbacks - Callbacks for the action.
   */
  handleDeleteVersion(
    version: VersionSchema,
    callbacks: IOHandlerCallback
  ): void;
}
