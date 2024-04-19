/**
 * The types of health checks on an artifact.
 */
export type HealthCheckType =
  | "contradiction"
  | "suggestion"
  | "unknown_concept"
  | "matched_concept"
  | "multi_matched_concept";

/**
 * Represents a health check on an artifact.
 */
interface HealthCheckSchema {
  /**
   * The type of health check.
   */
  type: HealthCheckType;
  /**
   * The message of the health check.
   */
  body: string;
}

/**
 * Represents a health check on an artifact based on a mentioned concept.
 */
interface ConceptHealthCheckSchema extends HealthCheckSchema {
  type: "matched_concept" | "unknown_concept";
  /**
   * The name of the concept.
   */
  name: string;
}

/**
 * Represents a health check on an artifact based on a contradiction.
 */
interface ContradictionHealthCheckSchema extends HealthCheckSchema {
  type: "contradiction";
  /**
   * The artifacts affected by the contradiction.
   */
  affectedArtifacts: string[];
}

/**
 * Represents a health check on an artifact based on multiple concepts.
 */
interface MultipleConceptHealthCheckSchema extends HealthCheckSchema {
  type: "multi_matched_concept";
  /**
   * The names of the matched concepts.
   */
  concepts: string[];
}

/**
 * Represents any type of health check on an artifact.
 */
export type AnyHealthCheckSchema =
  | ConceptHealthCheckSchema
  | ContradictionHealthCheckSchema
  | MultipleConceptHealthCheckSchema;

/**
 * Represents a collection of health checks on an artifact.
 */
export interface ArtifactHealthSchema {
  /**
   * The unique identifier of the artifact being checked.
   */
  artifactId: string;
  /**
   * The health checks on the artifact.
   */
  checks: AnyHealthCheckSchema[];
}
