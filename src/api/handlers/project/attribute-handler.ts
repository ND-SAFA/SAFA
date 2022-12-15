import {
  AttributeLayoutSchema,
  AttributeSchema,
  IOHandlerCallback,
} from "@/types";
import { attributesStore, logStore, projectStore } from "@/hooks";
import {
  createAttribute,
  createAttributeLayout,
  deleteAttribute,
  deleteAttributeLayout,
  editAttribute,
  editAttributeLayout,
} from "@/api";

/**
 * Creates or edits an attribute and updates the store.
 * @param attribute - The attribute to save.
 * @param isUpdate - Whether an existing attribute is being updated.
 * @param onSuccess - Called if the save is successful.
 * @param onError - Called if the save fails.
 * @param onComplete - Called after the action.
 */
export async function handleSaveAttribute(
  attribute: AttributeSchema,
  isUpdate: boolean,
  { onSuccess, onError, onComplete }: IOHandlerCallback
): Promise<void> {
  try {
    const projectId = projectStore.projectId;

    if (isUpdate) {
      const updatedAttribute = await editAttribute(projectId, attribute);

      attributesStore.updateAttribute(updatedAttribute);

      logStore.onSuccess(`Edited attribute: ${attribute.label}`);
    } else {
      const createdAttribute = await createAttribute(projectId, attribute);

      attributesStore.updateAttribute(createdAttribute);

      logStore.onSuccess(`Created attribute: ${attribute.label}`);
    }
    onSuccess?.();
  } catch (e) {
    logStore.onDevError(String(e));
    logStore.onError(`Unable to save attribute: ${attribute.label}`);
    onError?.(e as Error);
  } finally {
    onComplete?.();
  }
}

/**
 * Deletes an attribute and updates the store.
 * @param attribute - The attribute to delete.
 * @param onSuccess - Called if the delete is successful.
 * @param onError - Called if the delete fails.
 * @param onComplete - Called after the action.
 */
export function handleDeleteAttribute(
  attribute: AttributeSchema,
  { onSuccess, onError, onComplete }: IOHandlerCallback
): void {
  logStore.confirm(
    "Delete Attribute",
    `Are you sure you would like to delete "${attribute.label}"?`,
    async (isConfirmed: boolean) => {
      if (!isConfirmed) return;

      deleteAttribute(projectStore.projectId, attribute)
        .then(() => {
          attributesStore.deleteAttribute(attribute);
          logStore.onSuccess(`Deleted attribute: ${attribute.label}`);
          onSuccess?.();
        })
        .catch((e) => {
          logStore.onError(`Unable to delete attribute: ${attribute.label}`);
          onError?.(e);
        })
        .finally(onComplete);
    }
  );
}

/**
 * Creates or edits an attribute layout and updates the store.
 * @param layout - The attribute layout to save.
 * @param isUpdate - Whether an existing attribute layout is being updated.
 * @param onSuccess - Called if the save is successful.
 * @param onError - Called if the save fails.
 * @param onComplete - Called after the action.
 */
export async function handleSaveAttributeLayout(
  layout: AttributeLayoutSchema,
  isUpdate: boolean,
  { onSuccess, onError, onComplete }: IOHandlerCallback
): Promise<void> {
  try {
    const projectId = projectStore.projectId;

    if (isUpdate) {
      const updatedLayout = await editAttributeLayout(projectId, layout);

      attributesStore.updateLayout(updatedLayout);

      logStore.onSuccess(`Edited attribute layout: ${layout.name}`);
    } else {
      const createdLayout = await createAttributeLayout(projectId, layout);

      attributesStore.updateLayout(createdLayout);

      logStore.onSuccess(`Created attribute layout: ${layout.name}`);
    }
    onSuccess?.();
  } catch (e) {
    logStore.onDevError(String(e));
    logStore.onError(`Unable to save attribute layout: ${layout.name}`);
    onError?.(e as Error);
  } finally {
    onComplete?.();
  }
}

/**
 * Deletes an attribute layout layout and updates the store.
 * @param layout - The attribute layout to delete.
 * @param onSuccess - Called if the delete is successful.
 * @param onError - Called if the delete fails.
 * @param onComplete - Called after the action.
 */
export function handleDeleteAttributeLayout(
  layout: AttributeLayoutSchema,
  { onSuccess, onError, onComplete }: IOHandlerCallback
): void {
  logStore.confirm(
    "Delete Attribute Layout",
    `Are you sure you would like to delete "${layout.name}"?`,
    async (isConfirmed: boolean) => {
      if (!isConfirmed) return;

      deleteAttributeLayout(projectStore.projectId, layout)
        .then(() => {
          attributesStore.deleteLayout(layout);
          logStore.onSuccess(`Deleted attribute layout: ${layout.name}`);
          onSuccess?.();
        })
        .catch((e) => {
          logStore.onError(`Unable to delete attribute layout: ${layout.name}`);
          onError?.(e);
        })
        .finally(onComplete);
    }
  );
}
