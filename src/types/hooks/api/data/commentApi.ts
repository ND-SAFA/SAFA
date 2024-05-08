import { ComputedRef } from "vue";
import {
  AnyCommentSchema,
  ArtifactSchema,
  BasicCommentSchema,
  IOHandlerCallback,
} from "@/types";

/**
 * Represents actions that can be performed on the comment API.
 */
export interface CommentApiHook {
  /**
   * Whether the health checks are currently loading.
   */
  healthLoading: ComputedRef<boolean>;
  /**
   * Loads all comments for the given artifact.
   * @param artifactId - The ID of the artifact to get comments for.
   */
  handleLoadComments(artifactId: string): Promise<void>;

  /**
   * Adds a comment to the given artifact.
   * @param artifact - The artifact to add a comment to.
   * @param content - The content of the comment.
   * @param type - The type of comment to add.
   * @param callbacks - Callbacks to run after the comment is added.
   */
  handleAddComment(
    artifact: ArtifactSchema,
    content: string,
    type: "flag" | "conversation",
    callbacks?: IOHandlerCallback
  ): Promise<void>;

  /**
   * Resolves a comment on the given artifact.
   * @param artifact - The artifact to resolve a comment on.
   * @param comment - The comment to resolve.
   */
  handleResolveComment(
    artifact: ArtifactSchema,
    comment: AnyCommentSchema
  ): Promise<void>;

  /**
   * Edits a comment on the given artifact.
   * @param artifact - The artifact to edit a comment on.
   * @param comment - The comment to edit.
   * @param callbacks - Callbacks to run after the comment is edited.
   */
  handleEditComment(
    artifact: ArtifactSchema,
    comment: BasicCommentSchema,
    callbacks?: IOHandlerCallback
  ): Promise<void>;

  /**
   * Deletes a comment on the given artifact.
   * @param artifact - The artifact to delete a comment on.
   * @param commentId - The ID of the comment to delete.
   * @param callbacks - Callbacks to run after the comment is deleted.
   */
  handleDeleteComment(
    artifact: ArtifactSchema,
    commentId: string,
    callbacks?: IOHandlerCallback
  ): Promise<void>;
  handleLoadHealthChecks(artifact: ArtifactSchema): Promise<void>;
}
