/**
 * Defines a type of artifact in a project.
 */
export interface ArtifactTypeSchema {
  /**
   * The UUID for specific artifact type.
   */
  typeId: string;
  /**
   * The name of this type of artifacts.
   */
  name: string;
  /**
   * The icon that should be used to represent it.
   */
  icon: string;
}

/**
 * Enumerates any specific artifact types that are handled differently.
 */
export enum ReservedArtifactType {
  github = "GitHub File",
}
