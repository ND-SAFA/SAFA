import { defineStore } from "pinia";

import { IOHandlerCallback, LayoutApiHook } from "@/types";
import { useApi, documentStore, logStore, projectStore } from "@/hooks";
import { createLayout } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing layout API requests.
 */
export const useLayoutApi = defineStore("layoutApi", (): LayoutApiHook => {
  const layoutApi = useApi("layoutApi");

  async function handleRegenerate(
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
      {
        ...callbacks,
        useAppLoad: true,
        success: "The current layout has been updated.",
        error: "Unable to update the current layout.",
      }
    );
  }

  return { handleRegenerate };
});

export default useLayoutApi(pinia);
