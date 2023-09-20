import { ComputedRef, WritableComputedRef } from "vue";
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
   * The current loaded project.
   * - Reactively loads the current project when set.
   */
  currentProject: WritableComputedRef<IdentifierSchema | undefined>;
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
