import { defineStore } from "pinia";

import {
  AnyCommentSchema,
  ArtifactCommentsSchema,
  ArtifactSchema,
  BasicCommentSchema,
  DisplayableHealthCheckSchema,
  IconVariant,
  ThemeColor,
} from "@/types";
import { artifactSaveStore, artifactStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * A store for managing artifact comments, flags, and health checks.
 * Content for each artifact is added and cached as needed.
 */
export const useComments = defineStore("useComments", {
  state: () => ({
    /**
     * A map of artifact comments, flags, and health checks by artifact ID.
     */
    commentsByArtifactId: {} as Record<string, ArtifactCommentsSchema>,
    /**
     * A list of health checks for newly created artifacts.
     */
    newArtifactHealth: [] as AnyCommentSchema[],
  }),
  getters: {},
  actions: {
    /**
     * Returns comments and flags for a given artifact.
     * @param artifactId - The unique identifier of the artifact.
     * @param includeResolved - Whether to include resolved comments.
     * @returns The comments on the artifact.
     */
    getCommentsAndFlags(
      artifactId: string,
      includeResolved?: boolean
    ): BasicCommentSchema[] {
      const comments = this.commentsByArtifactId[artifactId]?.comments || [];
      const flags = this.commentsByArtifactId[artifactId]?.flags || [];

      return includeResolved
        ? [...flags, ...comments]
        : [...flags, ...comments].filter(
            (comment) => comment.status === "active"
          );
    },
    /**
     * Returns health checks for a given artifact.
     * @param artifactId - The unique identifier of the artifact.
     * @returns The health checks on the artifact.
     */
    getHealthChecks(artifactId: string): DisplayableHealthCheckSchema[] {
      const getArtifacts = (artifactIds: string[]) =>
        artifactIds
          .map(
            (id) =>
              artifactStore.getArtifactById(id) ||
              artifactStore.getArtifactByName(id) // TODO: remove after testing
          )
          .filter((artifact) => !!artifact) as ArtifactSchema[];

      const checkToDisplay = (
        checks: AnyCommentSchema[]
      ): DisplayableHealthCheckSchema[] =>
        checks
          .filter((comment) => comment.status !== "resolved")
          .map((health) => ({
            ...health,
            icon: ((): IconVariant => {
              switch (health.type) {
                case "contradiction":
                  return "health-conflict";
                case "cited_concept":
                case "predicted_concept":
                  return "health-concept";
                case "multi_matched_concept":
                  return "health-concept-multiple";
                case "undefined_concept":
                  return "health-unknown";
                default:
                  return "flag";
              }
            })(),
            color: ((): ThemeColor => {
              switch (health.type) {
                case "cited_concept":
                  return "positive";
                case "contradiction":
                  return "negative";
                default:
                  return "warning";
              }
            })(),
            artifacts: ((): ArtifactSchema[] => {
              switch (health.type) {
                case "cited_concept":
                case "predicted_concept":
                  return getArtifacts([health.conceptArtifactId]);
                case "contradiction":
                  return getArtifacts(health.artifactIds);
                case "multi_matched_concept":
                  return getArtifacts(health.conceptArtifactIds);
                default:
                  return [];
              }
            })(),
            concepts:
              health.type === "undefined_concept"
                ? [health.undefinedConcept]
                : [],
            action: () => {
              switch (health.type) {
                case "cited_concept":
                  return;
                case "predicted_concept":
                  return;
                case "undefined_concept":
                  return artifactSaveStore.openPanel({
                    isNewArtifact: true,
                    artifact: { name: health.undefinedConcept },
                    parentId: artifactId,
                  });
                case "contradiction":
                  return;
                case "multi_matched_concept":
                  return;
              }
            },
          }));

      if (artifactId) {
        return checkToDisplay([
          ...(this.commentsByArtifactId[artifactId]?.healthChecks || []),
          ...(this.commentsByArtifactId[artifactId]?.flags || []),
        ]);
      } else {
        return checkToDisplay(this.newArtifactHealth);
      }
    },
    /**
     * Adds comments, flags, and health checks for a given artifact.
     * @param artifactId - The unique identifier of the artifact.
     * @param comments - The comments, flags, and health checks to add.
     */
    addArtifact(artifactId: string, comments: ArtifactCommentsSchema): void {
      this.commentsByArtifactId[artifactId] = comments;
    },
    /**
     * Adds health checks for a given artifact.
     * @param artifactId - The unique identifier of the artifact.
     * @param healthChecks - The health checks to add.
     */
    addHealthChecks(
      artifactId: string,
      healthChecks: AnyCommentSchema[]
    ): void {
      this.newArtifactHealth = [];

      if (artifactId) {
        if (!this.commentsByArtifactId[artifactId]) {
          this.commentsByArtifactId[artifactId] = {
            artifactId,
            comments: [],
            flags: [],
            healthChecks: [],
          };
        }

        this.commentsByArtifactId[artifactId].healthChecks = healthChecks;
      } else {
        this.newArtifactHealth = healthChecks;
      }
    },
    /**
     * Adds a comment to an artifact.
     * @param artifactId - The unique identifier of the artifact.
     * @param comment - The comment to add.
     */
    addComment(artifactId: string, comment: BasicCommentSchema): void {
      if (!this.commentsByArtifactId[artifactId]) {
        this.commentsByArtifactId[artifactId] = {
          artifactId,
          comments: [],
          flags: [],
          healthChecks: [],
        };
      }

      if (comment.type === "conversation") {
        this.commentsByArtifactId[artifactId].comments.push(comment);
      } else {
        this.commentsByArtifactId[artifactId].flags.push(comment);
      }
    },
    /**
     * Edits a comment on an artifact.
     * @param artifactId - The unique identifier of the artifact.
     * @param comment - The comment that has been edited.
     */
    editComment(artifactId: string, comment: AnyCommentSchema): void {
      const comments =
        comment.type === "conversation"
          ? this.commentsByArtifactId[artifactId].comments
          : comment.type === "flag"
            ? this.commentsByArtifactId[artifactId].flags
            : this.commentsByArtifactId[artifactId].healthChecks;
      const index = comments.findIndex((c) => c.id === comment.id);

      if (index !== -1) {
        comments[index] = comment;
      }
    },
    /**
     * Deletes a comment from an artifact.
     * @param artifactId - The unique identifier of the artifact.
     * @param commentId - The unique identifier of the comment.
     */
    deleteComment(artifactId: string, commentId: string): void {
      const comments =
        this.commentsByArtifactId[artifactId].comments ||
        this.commentsByArtifactId[artifactId].flags;
      const index = comments.findIndex((c) => c.id === commentId);

      if (index !== -1) {
        comments.splice(index, 1);
      }
    },
  },
});

export default useComments(pinia);
