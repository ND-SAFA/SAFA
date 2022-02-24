/**
 * Defines an type of artifact in a project.
 */
export interface ArtifactType {
  /**
   * The UUID for specific artifact type.
   */
  typeId?: string;

  /**
   * The name of this type of artifacts.
   */
  name: string;
  /**
   * The icon that should be used to represent it.
   */
  icon: string;
}
