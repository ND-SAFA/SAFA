import { defineStore } from "pinia";

import { IOHandlerCallback } from "@/types";
import { useApi, documentStore, logStore, projectStore } from "@/hooks";
import { createLayout } from "@/api";
import { pinia } from "@/plugins";

export const useLayoutApi = defineStore("layoutApi", () => {
  const layoutApi = useApi("layoutApi");

  /**
   * Handles regenerating and storing the layout for the current project version and document.
   *
   * @param callbacks - Callbacks to handle the result of the operation.
   */
  async function handleRegenerateLayout(
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await layoutApi.handleRequest(
      async () => {
        const versionId = projectStore.versionId;
        const documentId = documentStore.currentId;

        logStore.onInfo("Regenerating the current layout.");

        const generatedLayouts = await createLayout(versionId, documentId);

        if (!documentId) {
          // Update the default layout.
          documentStore.updateBaseLayout(
            generatedLayouts.defaultDocumentLayout
          );
        } else {
          // Update the current document layout.
          Object.entries(generatedLayouts.documentLayoutMap).forEach(
            ([documentId, layout]) =>
              documentStore.updateDocumentLayout(documentId, layout)
          );
        }
      },
      callbacks,
      {
        useAppLoad: true,
        success: "The current layout has been updated.",
        error: "Unable to update the current layout.",
      }
    );
  }

  return { handleRegenerateLayout };
});

export default useLayoutApi(pinia);
