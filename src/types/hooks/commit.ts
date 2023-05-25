import { CommitSchema } from "@/types";

/**
 * Container for a commit and its revert used in commit module.
 */
export interface CommitHistory {
  /**
   * The original commit;
   */
  commit: CommitSchema;
  /**
   * The revert of the commit containing the states
   * before the commit is applied.
   */
  revert: CommitSchema;
}
