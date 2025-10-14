import { ComputedRef } from "vue";
import { IOHandlerCallback } from "@/types";

/**
 * A hook for calling get project API endpoints.
 */
export interface GetProjectApiHook {
  /**
   * Whether the get project request is loading.
   */
  loading: ComputedRef<boolean>;
  /**
   * Stores all projects for the current user.
   *
   * @param callbacks - The callbacks to call after the action.
   */
  handleLoadProjects(callbacks?: IOHandlerCallback): Promise<void>;
  /**
   * Loads the last stored project.
   */
  handleLoadRecent(): Promise<void>;
}
