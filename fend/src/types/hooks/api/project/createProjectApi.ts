import { ComputedRef } from "vue";
import { IOHandlerCallback, ProjectSchema } from "@/types";

/**
 * A hook for calling create project API endpoints.
 */
export interface CreateProjectApiHook {
  /**
   * Whether the create project request is loading.
   */
  loading: ComputedRef<boolean>;
  /**
   * Creates a new project, sets related app state, and logs the status.
   *
   * @param callbacks - The callbacks to call after the action.
   */
  handleImport(callbacks: IOHandlerCallback): Promise<void>;
  /**
   * Creates a new project from files, sets related app state, and logs the status.
   *
   * @param project - The project to create.
   * @param files - The files to upload.
   * @param summarize - Whether to summarize artifacts.
   * @param callbacks - The callbacks to use on success, error, and complete.
   */
  handleBulkImport(
    project: Pick<
      ProjectSchema,
      "projectId" | "name" | "description" | "projectVersion"
    >,
    files: File[],
    summarize: boolean,
    callbacks: IOHandlerCallback
  ): Promise<void>;
  /**
   * Imports a Jira project, sets related app state, and moves to the upload page.
   *
   * @param callbacks - The callbacks to call after the action.
   */
  handleJiraImport(callbacks: IOHandlerCallback): Promise<void>;
  /**
   * Imports a GitHub project, sets related app state, and moves to the upload page.
   *
   * @param callbacks - The callbacks to call after the action.
   */
  handleGitHubImport(callbacks: IOHandlerCallback): Promise<void>;
}
