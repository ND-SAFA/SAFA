import { ArtifactTypeSchema } from "@/types";

/**
 * A hook for calling artifact type API endpoints.
 */
export interface ArtifactTypeApiHook {
  /**
   * Creates or updates the given artifact type.
   *
   * @param artifactType - The artifact type to add or edit.
   */
  handleSave(artifactType: ArtifactTypeSchema): Promise<void>;
}
