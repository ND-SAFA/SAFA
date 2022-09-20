import { IOHandlerCallback } from "@/types";
import { appStore, documentStore, logStore, projectStore } from "@/hooks";
import { createLayout } from "@/api";

/**
 * Handles regenerating and storing the layout for the current project version and document.
 *
 * @param onSuccess - Called if the operation is successful.
 * @param onError - Called if the operation fails.
 */
export function handleRegenerateLayout({
  onSuccess,
  onError,
}: IOHandlerCallback): void {
  const versionId = projectStore.versionId;
  const documentId = documentStore.currentId;

  logStore.onInfo("Regenerating the current layout.");
  appStore.onLoadStart();

  createLayout(versionId, documentId)
    .then((generated) => {
      if (!documentId) {
        // Update the default layout.
        documentStore.updateBaseLayout(generated.defaultDocumentLayout);
      } else {
        // Update the current document layout.
        Object.entries(generated.documentLayoutMap).forEach(
          ([documentId, layout]) =>
            documentStore.updateDocumentLayout(documentId, layout)
        );
      }

      logStore.onSuccess("The current layout has been updated.");
      onSuccess?.();
    })
    .catch((e) => {
      logStore.onError("Unable to update the current layout.");
      logStore.onDevError(String(e));
      onError?.(e as Error);
    })
    .finally(() => appStore.onLoadEnd());
}
