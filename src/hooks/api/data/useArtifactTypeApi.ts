import { defineStore } from "pinia";

import { ArtifactTypeSchema, TimArtifactLevelSchema } from "@/types";
import { useApi, projectStore, typeOptionsStore } from "@/hooks";
import { pinia } from "@/plugins";
import { createArtifactType, editArtifactType } from "@/api/endpoints";

export const useArtifactTypeApi = defineStore("artifactTypeApi", () => {
  const artifactTypeApi = useApi("artifactTypeApi");

  /**
   * Creates or updates the given artifact type.
   *
   * @param artifactType - The artifact type to add or edit.
   */
  async function handleSave(artifactType: ArtifactTypeSchema): Promise<void> {
    await artifactTypeApi.handleRequest(
      async () => {
        const updatedArtifactType = artifactType.id
          ? await editArtifactType(projectStore.projectId, artifactType)
          : await createArtifactType(projectStore.projectId, artifactType);

        typeOptionsStore.addOrUpdateArtifactTypes([updatedArtifactType]);
      },
      {},
      {
        success: `Saved artifact type: ${artifactType.name}`,
        error: `Unable to save artifact type: ${artifactType.name}`,
      }
    );
  }

  /**
   * Updates the icon for an artifact type.
   *
   * @param artifactLevel - The artifact type to add or edit.
   */
  async function handleSaveIcon(
    artifactLevel: TimArtifactLevelSchema
  ): Promise<void> {
    const type = typeOptionsStore.allArtifactTypes.find(
      ({ id }) => id === artifactLevel.id
    );

    if (!type) return;

    typeOptionsStore.updateArtifactIcon(artifactLevel);
    await handleSave({ ...type, icon: artifactLevel.icon });
  }

  return { handleSave, handleSaveIcon };
});

export default useArtifactTypeApi(pinia);
