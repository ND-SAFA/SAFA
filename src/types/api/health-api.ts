/**
 * The set of health tasks that can be performed.
 */
export type HealthTask =
  | "contradiction"
  | "concept_matching"
  | "concept_extraction";

/**
 * Request used to perform health tasks.
 */
export interface HealthRequest {
  /**
   * ID of version to run health checks on.
   */
  versionId: string;
  /**
   * List of health tasks to perform on artifacts.
   */
  tasks: HealthTask[];
  /**
   * List of artifact types to include in health tasks.
   */
  artifactTypes: string[];
  /**
   * List of artifact ids to perform health tasks on.
   */
  artifactIds: string[];
}
