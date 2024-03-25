import { ComputedRef } from "vue";
import {
  IOHandlerCallback,
  ProjectSchema,
  TransferProjectSchema,
} from "@/types";

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
   * @param versionId - The version to download, if different from the currently loaded version.
   */
  handleDownload(fileType?: "csv" | "json", versionId?: string): Promise<void>;
  /**
   * Deletes a project, updates app state, and logs the status.
   *
   * @param callbacks - Callbacks for the action.
   */
  handleDelete(callbacks: IOHandlerCallback): Promise<void>;
  /**
   * Moves the current project to a new owner.
   *
   * @param newOwner - The new owner of the project.
   * @param callbacks - Callbacks for the action.
   */
  handleTransfer(
    newOwner: TransferProjectSchema,
    callbacks?: IOHandlerCallback
  ): Promise<void>;
}
