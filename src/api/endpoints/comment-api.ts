import {
  ArtifactCommentsSchema,
  ArtifactSchema,
  BasicCommentSchema,
  CreateCommentSchema,
  HealthCheckCollectionSchema,
} from "@/types";
import { ENABLED_FEATURES } from "@/util";
import { buildRequest } from "@/api";

const EXAMPLE_COMMENTS: ArtifactCommentsSchema = {
  artifactId: "",
  comments: [
    {
      id: "1",
      versionId: "1",
      content: "Has anyone had a chance to review this requirement yet?",
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
      versionId: "1",
      content: "There is a potential issue with this requirement.",
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
      versionId: "1",
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
      versionId: "1",
      content: "This requirement references the following concept.",
      userId: "tim@safa.ai",
      status: "active",
      type: "cited_concept",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      conceptArtifactId: "Launch Services",
    },
    {
      id: "13",
      versionId: "1",
      content: "`Product Refresh Rate` not found in the project vocabulary.",
      userId: "tim@safa.ai",
      status: "active",
      type: "undefined_concept",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      undefinedConcept: "Product Refresh Rate",
    },
    {
      id: "13",
      versionId: "1",
      content: "DCP matched with multiple concepts. Which did you mean?",
      userId: "tim@safa.ai",
      status: "active",
      type: "multi_matched_concept",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      conceptArtifactIds: [
        "Data Collection Platforms (DCP)",
        "Data Collection System (DCS)",
      ],
    },
  ],
};

/**
 * Get the comments for an artifact.
 * @param artifactId - The unique identifier of the artifact.
 * @returns The comments for the artifact.
 */
export async function getArtifactComments(
  artifactId: string
): Promise<ArtifactCommentsSchema> {
  if (ENABLED_FEATURES.NASA_ARTIFACT_COMMENT_MOCKUP) {
    return { ...EXAMPLE_COMMENTS, artifactId };
  }

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
  if (ENABLED_FEATURES.NASA_ARTIFACT_COMMENT_MOCKUP) {
    return {
      id: Math.random().toString(),
      versionId: comment.versionId,
      content: comment.content,
      type: comment.type,
      userId: "tim@safa.ai",
      createdAt: new Date(Date.now()).toISOString(),
      updatedAt: new Date(Date.now()).toISOString(),
      status: "active",
    };
  }

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
  if (ENABLED_FEATURES.NASA_ARTIFACT_COMMENT_MOCKUP) {
    return comment;
  }

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
  if (ENABLED_FEATURES.NASA_ARTIFACT_COMMENT_MOCKUP) {
    return;
  }

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
  if (ENABLED_FEATURES.NASA_ARTIFACT_COMMENT_MOCKUP) {
    return;
  }

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
  if (ENABLED_FEATURES.NASA_ARTIFACT_COMMENT_MOCKUP) {
    return EXAMPLE_COMMENTS;
  }

  return buildRequest<HealthCheckCollectionSchema, "versionId", ArtifactSchema>(
    "healthChecks",
    { versionId }
  ).post(artifact);
}
