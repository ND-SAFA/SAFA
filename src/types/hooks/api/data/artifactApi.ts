import { ComputedRef, Ref } from "vue";
import { ArtifactSchema, IOHandlerCallback } from "@/types";

/**
 * A hook for calling artifact API endpoints.
 */
export interface ArtifactApiHook {
  /**
   * Whether the artifact is currently being saved.
   */
  saveLoading: ComputedRef<boolean>;
  /**
   * Whether the artifact is currently being deleted.
   */
  deleteLoading: ComputedRef<boolean>;
  /**
   * Whether the artifact name is currently being verified.
   */
  nameLoading: Ref<boolean>;
  /**
   * An error message about the artifact name, or false if there is no error.
   */
  nameError: ComputedRef<string | false>;

  /**
   * Verifies that the edited artifact's name is unique.
   */
  handleCheckName(): Promise<void>;
  /**
   * Creates or updates an artifact, and updates app state.
   *
   * @param artifact - The artifact to create.
   * @param isUpdate - Whether this operation should label this commit as
   * updating a previously existing artifact.
   * @param parentArtifacts - The parent artifacts to link to.
   * @param childArtifacts - The child artifacts to link to.
   * @param callbacks - Callbacks to run after the action.
   */
  handleSave(
    artifact: ArtifactSchema,
    isUpdate: boolean,
    parentArtifacts?: ArtifactSchema[],
    childArtifacts?: ArtifactSchema[],
    callbacks?: IOHandlerCallback
  ): Promise<void>;
  /**
   * Deletes an artifact, and updates the app state.
   *
   * @param artifact  - The artifact to delete.
   * @param callbacks - Callbacks to run after the action.
   */
  handleDelete(artifact: ArtifactSchema, callbacks?: IOHandlerCallback): void;
}
