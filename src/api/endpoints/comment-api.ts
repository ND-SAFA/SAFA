import {
  ArtifactCommentsSchema,
  ArtifactSchema,
  BasicCommentSchema,
  CreateCommentSchema,
  HealthCheckCollectionSchema,
} from "@/types";
import { buildRequest } from "@/api";

/**
 * Get the comments for an artifact.
 * @param artifactId - The unique identifier of the artifact.
 * @returns The comments for the artifact.
 */
export async function getArtifactComments(
  artifactId: string
): Promise<ArtifactCommentsSchema> {
  return buildRequest<ArtifactCommentsSchema, "artifactId">(
    "commentCollection",
    {
      artifactId,
    }
  ).get();
}

/**
 * Create a comment on an artifact.
 * @param artifactId - The unique identifier of the artifact.
 * @param comment - The comment to create.
 * @returns The comment created.
 */
export async function createArtifactComment(
  artifactId: string,
  comment: CreateCommentSchema
): Promise<BasicCommentSchema> {
  return buildRequest<BasicCommentSchema, "artifactId", CreateCommentSchema>(
    "commentCollection",
    { artifactId }
  ).post(comment);
}

/**
 * Edit a comment on an artifact.
 * @param artifactId - The unique identifier of the artifact.
 * @param comment - The comment to edit.
 * @returns The comment edited.
 */
export async function editArtifactComment(
  artifactId: string,
  comment: BasicCommentSchema
): Promise<BasicCommentSchema> {
  return buildRequest<
    BasicCommentSchema,
    "artifactId" | "commentId",
    BasicCommentSchema
  >("commentContent", { artifactId, commentId: comment.id }).put(comment);
}

/**
 * Delete a comment on an artifact.
 * @param artifactId - The unique identifier of the artifact.
 * @param commentId - The unique identifier of the comment.
 */
export async function deleteArtifactComment(
  artifactId: string,
  commentId: string
): Promise<void> {
  return buildRequest<void, "artifactId" | "commentId">("comment", {
    artifactId,
    commentId,
  }).delete();
}

/**
 * Resolve a comment on an artifact.
 * @param artifactId - The unique identifier of the artifact.
 * @param commentId - The unique identifier of the comment.
 */
export async function resolveArtifactComment(
  artifactId: string,
  commentId: string
): Promise<void> {
  return buildRequest<void, "artifactId" | "commentId">("commentResolve", {
    artifactId,
    commentId,
  }).put();
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
  return buildRequest<HealthCheckCollectionSchema, "versionId", ArtifactSchema>(
    "healthChecks",
    { versionId }
  ).post(artifact);
}
