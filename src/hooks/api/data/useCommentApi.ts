import { defineStore } from "pinia";

import { computed } from "vue";
import {
  AnyCommentSchema,
  ArtifactSchema,
  BasicCommentSchema,
  CommentApiHook,
  IOHandlerCallback,
} from "@/types";
import { commentStore, logStore, projectStore, useApi } from "@/hooks";
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
    const healthApi = useApi("healthApi");

    const healthLoading = computed(() => healthApi.loading);

    async function handleLoadComments(artifactId: string): Promise<void> {
      await commentApi.handleRequest(async () => {
        commentStore.addArtifact(
          artifactId,
          await getArtifactComments(artifactId)
        );
      });
    }

    async function handleAddComment(
      artifact: ArtifactSchema,
      content: string,
      type: "flag" | "conversation",
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      await commentApi.handleRequest(
        async () => {
          commentStore.addComment(
            artifact.id,
            await createArtifactComment(artifact.id, {
              content,
              type,
              versionId: projectStore.versionId,
            })
          );
        },
        {
          ...callbacks,
          success: `Comment has been added: ${artifact.name}`,
          error: `Unable to add comment: ${artifact.name}`,
        }
      );
    }

    async function handleResolveComment(
      artifact: ArtifactSchema,
      comment: AnyCommentSchema
    ): Promise<void> {
      await commentApi.handleRequest(
        async () => {
          await resolveArtifactComment(artifact.id, comment.id);

          comment.status = "resolved";

          commentStore.editComment(artifact.id, comment);
        },
        {
          success: `Comment has been resolved: ${artifact.name}`,
          error: `Unable to resolve comment: ${artifact.name}`,
        }
      );
    }

    async function handleEditComment(
      artifact: ArtifactSchema,
      comment: BasicCommentSchema,
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      await commentApi.handleRequest(
        async () => {
          commentStore.editComment(
            artifact.id,
            await editArtifactComment(artifact.id, comment)
          );
        },
        {
          ...callbacks,
          success: `Comment has been edited: ${artifact.name}`,
          error: `Unable to edit comment: ${artifact.name}`,
        }
      );
    }

    async function handleDeleteComment(
      artifact: ArtifactSchema,
      commentId: string,
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      logStore.confirm(
        "Delete Comment",
        "Are you sure you want to delete this comment?",
        async () => {
          await commentApi.handleRequest(
            async () => {
              await deleteArtifactComment(artifact.id, commentId);

              commentStore.deleteComment(artifact.id, commentId);
            },
            {
              ...callbacks,
              success: `Comment has been deleted: ${artifact.name}`,
              error: `Unable to delete comment: ${artifact.name}`,
            }
          );
        }
      );
    }

    async function handleLoadHealthChecks(
      artifact: ArtifactSchema
    ): Promise<void> {
      await healthApi.handleRequest(
        async () => {
          commentStore.addHealthChecks(
            artifact.id,
            (await generateArtifactHealth(projectStore.versionId, artifact))
              .healthChecks
          );
        },
        {
          success: `Health checks have been generated: ${artifact.name}`,
          error: `Unable to generate health checks: ${artifact.name}`,
        }
      );
    }

    return {
      healthLoading,
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
