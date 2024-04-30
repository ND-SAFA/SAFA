import { defineStore } from "pinia";

import {
  ArtifactSchema,
  CommentSchema,
  CommentType,
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
export const useCommentApi = defineStore("useCommentApi", () => {
  const commentApi = useApi("commentApi");

  async function handleLoadComments(artifactId: string): Promise<void> {
    await commentApi.handleRequest(async () => {
      commentStore.addArtifact(
        artifactId,
        await getArtifactComments(projectStore.versionId, artifactId)
      );
    });
  }

  async function handleAddComment(
    artifactId: string,
    content: string,
    type: CommentType,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await commentApi.handleRequest(async () => {
      commentStore.addComment(
        artifactId,
        await createArtifactComment(projectStore.versionId, artifactId, {
          content,
          type,
        })
      );
    }, callbacks);
  }

  async function handleResolveComment(
    artifactId: string,
    comment: CommentSchema
  ): Promise<void> {
    await commentApi.handleRequest(async () => {
      await resolveArtifactComment(
        projectStore.versionId,
        artifactId,
        comment.id
      );

      comment.status = "resolved";

      commentStore.editComment(artifactId, comment);
    });
  }

  async function handleEditComment(
    artifactId: string,
    comment: CommentSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await commentApi.handleRequest(async () => {
      commentStore.editComment(
        artifactId,
        await editArtifactComment(projectStore.versionId, artifactId, comment)
      );
    }, callbacks);
  }

  async function handleDeleteComment(
    artifactId: string,
    commentId: string,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await commentApi.handleRequest(async () => {
      await deleteArtifactComment(
        projectStore.versionId,
        artifactId,
        commentId
      );

      commentStore.deleteComment(artifactId, commentId);
    }, callbacks);
  }

  async function handleLoadHealthChecks(
    artifact: ArtifactSchema
  ): Promise<void> {
    await commentApi.handleRequest(async () => {
      commentStore.addArtifact(
        artifact.id,
        await generateArtifactHealth(projectStore.versionId, artifact)
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
});

export default useCommentApi(pinia);
