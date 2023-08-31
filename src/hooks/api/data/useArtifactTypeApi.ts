import { defineStore } from "pinia";

import { ArtifactTypeSchema } from "@/types";
import { useApi, projectStore, timStore } from "@/hooks";
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
        const updatedArtifactType = artifactType.typeId
          ? await editArtifactType(projectStore.projectId, artifactType)
          : await createArtifactType(projectStore.projectId, artifactType);

        timStore.addOrUpdateArtifactTypes([
          {
            ...updatedArtifactType,
            count: artifactType.count,
          },
        ]);
      },
      {
        success: `Saved artifact type: ${artifactType.name}`,
        error: `Unable to save artifact type: ${artifactType.name}`,
      }
    );
  }

  return { handleSave };
});

export default useArtifactTypeApi(pinia);
