/**
 * Represents the type of user comment on an artifact.
 */
export type CommentType =
  | "warning" // Resolution is necessary
  | "conversation"; // Resolution is optional

/**
 * Represents the status of a user comment on an artifact.
 */
export type CommentStatus = "active" | "resolved";

/**
 * Represents a user comment on an artifact.
 */
export interface CommentSchema {
  /**
   * Unique identifier for the comment.
   */
  id: string;
  /**
   * The content of the comment.
   */
  content: string;
  /**
   * The user who published the comment.
   */
  userId: string;
  /**
   * The status of the comment.
   */
  status: CommentStatus;
  /**
   * The type of the comment.
   */
  type: CommentType;
  /**
   * The date and time the comment was created.
   */
  createdAt: string;
  /**
   * The date and time the comment was last edited.
   */
  lastEditedAt: string;
}

/**
 * Represents a collection of comments and flags on an artifact.
 */
export interface ArtifactCommentsSchema {
  /**
   * The unique identifier of the artifact.
   */
  artifactId: string;
  /**
   * The comments on the artifact.
   */
  comments: CommentSchema[];
  /**
   * The flags on the artifact.
   */
  flags: CommentSchema[];
}
