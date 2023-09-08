import { ComputedRef } from "vue";
import { IOHandlerCallback, TeamSchema } from "@/types";

/**
 * A hook for calling team API endpoints.
 */
export interface TeamApiHook {
  /**
   * Whether the create team request is loading.
   */
  createTeamApiLoading: ComputedRef<boolean>;
  /**
   * Whether the edit team request is loading.
   */
  editTeamApiLoading: ComputedRef<boolean>;
  /**
   * Whether the delete team request is loading.
   */
  deleteTeamApiLoading: ComputedRef<boolean>;
  /**
   * Creates a new team.
   *
   * @param team - The team to create.
   * @param callbacks - The callbacks to call after the action.
   */
  handleCreate(team: TeamSchema, callbacks?: IOHandlerCallback): Promise<void>;
  /**
   * Edits a team.
   *
   * @param team - The team to edit.
   * @param callbacks - The callbacks to call after the action.
   */
  handleEdit(team: TeamSchema, callbacks?: IOHandlerCallback): Promise<void>;
  /**
   * Deletes a team.
   *
   * @param team - The team to delete.
   * @param callbacks - The callbacks to call after the action.
   */
  handleDelete(team: TeamSchema, callbacks?: IOHandlerCallback): Promise<void>;
}
