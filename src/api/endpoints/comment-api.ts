import {
  ArtifactCommentsSchema,
  ArtifactSchema,
  CommentSchema,
  HealthCheckCollectionSchema,
} from "@/types";
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
      id: "11",
      content: "MRD1258 indicates a product refresh rate of 20 seconds.",
      userId: "tim@safa.ai",
      status: "active",
      type: "contradiction",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      artifactIds: ["MRD1258"],
    },
    {
      id: "12",
      content:
        "Consider adding the entity or noun that this requirement applies to.",
      userId: "tim@safa.ai",
      status: "active",
      type: "suggestion",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      conceptName: "Entity",
    },
    {
      id: "13",
      content: "Product Refresh Rate not found in the project vocabulary.",
      userId: "tim@safa.ai",
      status: "active",
      type: "undefined_concept",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      undefinedConcept: {} as ArtifactSchema,
    },
    {
      id: "13",
      content: "SPOT matched with multiple concepts. Which did you mean?",
      userId: "tim@safa.ai",
      status: "active",
      type: "multi_matched_concept",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      concepts: [
        "System Performance and Operation Test",
        "Satellite Pour l'Observation de la Terre",
      ],
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
): Promise<HealthCheckCollectionSchema> {
  if (ENABLED_FEATURES.NASA_ARTIFACT_COMMENT_MOCKUP) {
    console.log("Generating health checks for artifact:", artifact.id);
    return EXAMPLE_COMMENTS;
  }

  return buildRequest<HealthCheckCollectionSchema, "versionId", ArtifactSchema>(
    "generateHealthChecks",
    { versionId }
  ).post(artifact);
}
