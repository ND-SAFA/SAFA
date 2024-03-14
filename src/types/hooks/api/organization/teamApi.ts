import { ComputedRef } from "vue";
import { IOHandlerCallback, TeamSchema } from "@/types";

/**
 * A hook for calling team API endpoints.
 */
export interface TeamApiHook {
  /**
   * Whether the save team request is loading.
   */
  saveTeamApiLoading: ComputedRef<boolean>;
  /**
   * Whether the delete team request is loading.
   */
  deleteTeamApiLoading: ComputedRef<boolean>;
  /**
   * Loads the projects for the current team.
   */
  handleLoadState(): Promise<void>;
  /**
   * Creates a new team or updates an existing one.
   *
   * @param team - The team to save.
   * @param callbacks - The callbacks to call after the action.
   */
  handleSave(team: TeamSchema, callbacks?: IOHandlerCallback): Promise<void>;
  /**
   * Deletes a team.
   *
   * @param team - The team to delete.
   * @param callbacks - The callbacks to call after the action.
   */
  handleDelete(team: TeamSchema, callbacks?: IOHandlerCallback): Promise<void>;
}
