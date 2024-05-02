import { defineStore } from "pinia";

import {
  ArtifactSchema,
  BasicCommentSchema,
  CommentApiHook,
  IOHandlerCallback,
} from "@/types";
import { commentStore, projectStore, useApi } from "@/hooks";
import {
  createArtifactComment,
  deleteArtifactComment,
  editArtifactComment,
  generateArtifactHealth,
  getArtifactComments,
  resolveArtifactComment,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * A store for managing artifact comments, flags, and health checks API.
 */
export const useCommentApi = defineStore(
  "useCommentApi",
  (): CommentApiHook => {
    const commentApi = useApi("commentApi");

    async function handleLoadComments(artifactId: string): Promise<void> {
      await commentApi.handleRequest(async () => {
        commentStore.addArtifact(
          artifactId,
          await getArtifactComments(artifactId)
        );
      });
    }

    async function handleAddComment(
      artifactId: string,
      content: string,
      type: "flag" | "conversation",
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      await commentApi.handleRequest(async () => {
        commentStore.addComment(
          artifactId,
          await createArtifactComment(artifactId, {
            content,
            type,
            versionId: projectStore.versionId,
          })
        );
      }, callbacks);
    }

    async function handleResolveComment(
      artifactId: string,
      comment: BasicCommentSchema
    ): Promise<void> {
      await commentApi.handleRequest(async () => {
        await resolveArtifactComment(artifactId, comment.id);

        comment.status = "resolved";

        commentStore.editComment(artifactId, comment);
      });
    }

    async function handleEditComment(
      artifactId: string,
      comment: BasicCommentSchema,
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      await commentApi.handleRequest(async () => {
        commentStore.editComment(
          artifactId,
          await editArtifactComment(artifactId, comment)
        );
      }, callbacks);
    }

    async function handleDeleteComment(
      artifactId: string,
      commentId: string,
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      await commentApi.handleRequest(async () => {
        await deleteArtifactComment(artifactId, commentId);

        commentStore.deleteComment(artifactId, commentId);
      }, callbacks);
    }

    async function handleLoadHealthChecks(
      artifact: ArtifactSchema
    ): Promise<void> {
      await commentApi.handleRequest(async () => {
        commentStore.addHealthChecks(
          artifact.id,
          (await generateArtifactHealth(projectStore.versionId, artifact))
            .healthChecks
        );
      });
    }

    return {
      handleLoadComments,
      handleAddComment,
      handleResolveComment,
      handleEditComment,
      handleDeleteComment,
      handleLoadHealthChecks,
    };
  }
);

export default useCommentApi(pinia);
