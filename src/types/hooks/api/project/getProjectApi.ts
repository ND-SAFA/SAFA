import { ComputedRef, Ref, WritableComputedRef } from "vue";
import { IdentifierSchema, IOHandlerCallback } from "@/types";

/**
 * A hook for calling get project API endpoints.
 */
export interface GetProjectApiHook {
  /**
   * Whether the get project request is loading.
   */
  loading: ComputedRef<boolean>;
  /**
   * All projects for the current user.
   */
  allProjects: Ref<IdentifierSchema[]>;
  /**
   * All projects for the current user except the current project.
   */
  unloadedProjects: ComputedRef<IdentifierSchema[]>;
  /**
   * The current loaded project.
   * - Reactively loads the current project when set.
   */
  currentProject: WritableComputedRef<IdentifierSchema | undefined>;
  /**
   * Adds or replaces a project in the project list.
   *
   * @param project - The project to add.
   */
  addProject(project: IdentifierSchema): void;
  /**
   * Stores all projects for the current user.
   *
   * @param callbacks - The callbacks to call after the action.
   */
  handleReload(callbacks?: IOHandlerCallback): Promise<void>;
  /**
   * Loads the last stored project.
   */
  handleLoadRecent(): Promise<void>;
}
