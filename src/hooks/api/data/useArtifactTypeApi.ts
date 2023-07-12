import { defineStore } from "pinia";

import { ArtifactTypeSchema, TimArtifactLevelSchema } from "@/types";
import { useApi, projectStore, typeOptionsStore } from "@/hooks";
import { pinia } from "@/plugins";
import { saveArtifactType } from "@/api/endpoints";

export const useArtifactTypeApi = defineStore("artifactTypeApi", () => {
  const artifactTypeApi = useApi("artifactTypeApi");

  /**
   * Creates or updates the given artifact type.
   *
   * @param artifactType - The artifact type to add or edit.
   */
  async function handleSave(artifactType: ArtifactTypeSchema): Promise<void> {
    await artifactTypeApi.handleRequest(async () => {
      const updatedArtifactType = await saveArtifactType(
        projectStore.projectId,
        artifactType
      );

      typeOptionsStore.addOrUpdateArtifactTypes([updatedArtifactType]);
    });
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
