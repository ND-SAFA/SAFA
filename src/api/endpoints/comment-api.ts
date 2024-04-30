import { comment } from "postcss";
import { ArtifactCommentsSchema, ArtifactSchema, CommentSchema } from "@/types";
import { ENABLED_FEATURES } from "@/util";
import { buildRequest } from "@/api";

const EXAMPLE_COMMENTS: ArtifactCommentsSchema = {
  artifactId: "",
  comments: [
    {
      id: "1",
      content:
        "Hello people, this is a super long comment that should wrap to multiple lines.",
      userId: "tim@safa.ai",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      status: "active",
      type: "conversation",
    },
  ],
  flags: [
    {
      id: "2",
      content: "Oh boy there's a flag",
      userId: "tim@safa.ai",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      status: "active",
      type: "flag",
    },
  ],
  healthChecks: [
    {
      id: "1",
      content: "[Matched concept]",
      userId: "tim@safa.ai",
      status: "active",
      type: "matched_concept",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      name: "[Concept]",
    },
    {
      id: "2",
      content: "[Conflicting Requirement]",
      userId: "tim@safa.ai",
      status: "active",
      type: "contradiction",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      affectedArtifacts: ["1", "2"],
    },
    {
      id: "3",
      content: "[Multiple Concept]",
      userId: "tim@safa.ai",
      status: "active",
      type: "multi_matched_concept",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      concepts: ["[Concept 1]", "[Concept 2]"],
    },
  ],
};

/**
 * Get the comments for an artifact.
 * @param versionId - The unique identifier of the version.
 * @param artifactId - The unique identifier of the artifact.
 * @returns The comments for the artifact.
 */
export async function getArtifactComments(
  versionId: string,
  artifactId: string
): Promise<ArtifactCommentsSchema> {
  if (ENABLED_FEATURES.NASA_ARTIFACT_COMMENT_MOCKUP) {
    return { ...EXAMPLE_COMMENTS, artifactId };
  }

  return buildRequest<ArtifactCommentsSchema, "versionId" | "artifactId">(
    "getComments",
    { versionId, artifactId }
  ).get();
}

/**
 * Create a comment on an artifact.
 * @param versionId - The unique identifier of the version.
 * @param artifactId - The unique identifier of the artifact.
 * @param comment - The comment to create.
 * @returns The comment created.
 */
export async function createArtifactComment(
  versionId: string,
  artifactId: string,
  comment: Pick<CommentSchema, "content" | "type">
): Promise<CommentSchema> {
  if (ENABLED_FEATURES.NASA_ARTIFACT_COMMENT_MOCKUP) {
    return {
      id: Math.random().toString(),
      content: comment.content,
      type: comment.type,
      userId: "tim@safa.ai",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      status: "active",
    };
  }

  return buildRequest<
    CommentSchema,
    "versionId" | "artifactId",
    Pick<CommentSchema, "content" | "type">
  >("createComment", { versionId, artifactId }).post(comment);
}

/**
 * Edit a comment on an artifact.
 * @param versionId - The unique identifier of the version.
 * @param artifactId - The unique identifier of the artifact.
 * @param comment - The comment to edit.
 * @returns The comment edited.
 */
export async function editArtifactComment(
  versionId: string,
  artifactId: string,
  comment: CommentSchema
): Promise<CommentSchema> {
  if (ENABLED_FEATURES.NASA_ARTIFACT_COMMENT_MOCKUP) {
    return comment;
  }

  return buildRequest<
    CommentSchema,
    "versionId" | "artifactId" | "commentId",
    CommentSchema
  >("editComment", { versionId, artifactId, commentId: comment.id }).put(
    comment
  );
}

/**
 * Delete a comment on an artifact.
 * @param versionId - The unique identifier of the version.
 * @param artifactId - The unique identifier of the artifact.
 * @param commentId - The unique identifier of the comment.
 */
export async function deleteArtifactComment(
  versionId: string,
  artifactId: string,
  commentId: string
): Promise<void> {
  if (ENABLED_FEATURES.NASA_ARTIFACT_COMMENT_MOCKUP) {
    return;
  }

  return buildRequest<void, "versionId" | "artifactId" | "commentId">(
    "deleteComment",
    { versionId, artifactId, commentId }
  ).delete();
}

/**
 * Resolve a comment on an artifact.
 * @param versionId - The unique identifier of the version.
 * @param artifactId - The unique identifier of the artifact.
 * @param commentId - The unique identifier of the comment.
 */
export async function resolveArtifactComment(
  versionId: string,
  artifactId: string,
  commentId: string
): Promise<void> {
  if (ENABLED_FEATURES.NASA_ARTIFACT_COMMENT_MOCKUP) {
    return;
  }

  return buildRequest<void, "versionId" | "artifactId" | "commentId">(
    "resolveComment",
    { versionId, artifactId, commentId }
  ).post();
}

/**
 * Generate health checks for an artifact.
 * @param versionId - The unique identifier of the version.
 * @param artifact - The artifact to generate health checks for.
 * @returns The health checks for the artifact.
 */
export async function generateArtifactHealth(
  versionId: string,
  artifact: ArtifactSchema
): Promise<ArtifactCommentsSchema> {
  if (ENABLED_FEATURES.NASA_ARTIFACT_COMMENT_MOCKUP) {
    return EXAMPLE_COMMENTS;
  }

  return buildRequest<ArtifactCommentsSchema, "versionId", ArtifactSchema>(
    "generateHealthChecks",
    { versionId }
  ).post(artifact);
}
