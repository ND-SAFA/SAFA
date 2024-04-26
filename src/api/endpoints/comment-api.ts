import { ArtifactCommentsSchema, ArtifactSchema, CommentSchema } from "@/types";
import { buildRequest } from "@/api";

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
  comment: CommentSchema
): Promise<CommentSchema> {
  return buildRequest<CommentSchema, "versionId" | "artifactId", CommentSchema>(
    "createComment",
    { versionId, artifactId }
  ).post(comment);
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
export function generateArtifactHealth(
  versionId: string,
  artifact: ArtifactSchema
): Promise<ArtifactCommentsSchema> {
  return buildRequest<ArtifactCommentsSchema, "versionId", ArtifactSchema>(
    "generateHealthChecks",
    { versionId }
  ).post(artifact);
}
