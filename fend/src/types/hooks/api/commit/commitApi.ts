import { CommitSchema } from "@/types";
import { CommitBuilder } from "@/util";

/**
 * A hook for calling commit API endpoints.
 */
export interface CommitApiHook {
  /**
   * Saves commit to the application store, and persist the commit.
   *
   * @param commitOrCb - The commit to save, or a callback to create it.
   * @return The saved commit.
   */
  handleSave(
    commitOrCb: CommitSchema | ((builder: CommitBuilder) => CommitBuilder)
  ): Promise<CommitSchema | undefined>;
  /**
   * Undoes the last commit.
   */
  handleUndo(): Promise<void>;
  /**
   * Reattempts the last undone commit.
   */
  handleRedo(): Promise<void>;
}
