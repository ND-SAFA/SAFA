import { defineStore } from "pinia";

import {
  AttributeLayoutSchema,
  AttributeSchema,
  IOHandlerCallback,
} from "@/types";
import { useApi, attributesStore, logStore, projectStore } from "@/hooks";
import {
  createAttribute,
  createAttributeLayout,
  deleteAttribute,
  deleteAttributeLayout,
  editAttribute,
  editAttributeLayout,
} from "@/api";
import { pinia } from "@/plugins";
export const useAttributeApi = defineStore("attributeApi", () => {
  const attributeApi = useApi("attributeApi");
  const attributeLayoutApi = useApi("attributeLayoutApi");

  /**
   * Creates or edits an attribute and updates the store.
   *
   * @param attribute - The attribute to save.
   * @param isUpdate - Whether an existing attribute is being updated.
   * @param callbacks - Callbacks to call after the action.
   */
  async function handleSaveAttribute(
    attribute: AttributeSchema,
    isUpdate: boolean,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await attributeApi.handleRequest(
      async () => {
        const projectId = projectStore.projectId;

        if (isUpdate) {
          const updatedAttribute = await editAttribute(projectId, attribute);

          attributesStore.updateAttribute(updatedAttribute);
        } else {
          const createdAttribute = await createAttribute(projectId, attribute);

          attributesStore.updateAttribute(createdAttribute);
        }
      },
      callbacks,
      {
        success: isUpdate
          ? `Edited attribute: ${attribute.label}`
          : `Created attribute: ${attribute.label}`,
        error: `Unable to save attribute: ${attribute.label}`,
      }
    );
  }

  /**
   * Deletes an attribute and updates the store.
   *
   * @param attribute - The attribute to delete.
   * @param callbacks - Callbacks to call after the action.
   */
  async function handleDeleteAttribute(
    attribute: AttributeSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await logStore.confirm(
      "Delete Attribute",
      `Are you sure you would like to delete "${attribute.label}"?`,
      async (isConfirmed: boolean) => {
        if (!isConfirmed) return;

        await attributeApi.handleRequest(
          async () => {
            await deleteAttribute(projectStore.projectId, attribute);

            attributesStore.deleteAttribute(attribute);
          },
          callbacks,
          {
            success: `Deleted attribute: ${attribute.label}`,
            error: `Unable to delete attribute: ${attribute.label}`,
          }
        );
      }
    );
  }

  /**
   * Creates or edits an attribute layout and updates the store.
   *
   * @param layout - The attribute layout to save.
   * @param isUpdate - Whether an existing attribute layout is being updated.
   * @param callbacks - Callbacks to call after the action.
   */
  async function handleSaveAttributeLayout(
    layout: AttributeLayoutSchema,
    isUpdate: boolean,
    callbacks: IOHandlerCallback<AttributeLayoutSchema> = {}
  ): Promise<void> {
    await attributeLayoutApi.handleRequest(
      async () => {
        const projectId = projectStore.projectId;

        const savedLayout = isUpdate
          ? await editAttributeLayout(projectId, layout)
          : await createAttributeLayout(projectId, layout);

        attributesStore.updateLayout(savedLayout);

        return savedLayout;
      },
      callbacks,
      {
        success: isUpdate
          ? `Edited attribute layout: ${layout.name}`
          : `Created attribute layout: ${layout.name}`,
        error: `Unable to save attribute layout: ${layout.name}`,
      }
    );
  }

  /**
   * Deletes an attribute layout and updates the store.
   *
   * @param layout - The attribute layout to delete.
   * @param callbacks - Callbacks to call after the action.
   */
  async function handleDeleteAttributeLayout(
    layout: AttributeLayoutSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await logStore.confirm(
      "Delete Attribute Layout",
      `Are you sure you would like to delete "${layout.name}"?`,
      async (isConfirmed: boolean) => {
        if (!isConfirmed) return;

        await attributeLayoutApi.handleRequest(
          async () => {
            await deleteAttributeLayout(projectStore.projectId, layout);

            attributesStore.deleteLayout(layout);
          },
          callbacks,
          {
            success: `Deleted attribute layout: ${layout.name}`,
            error: `Unable to delete attribute layout: ${layout.name}`,
          }
        );
      }
    );
  }

  return {
    handleSaveAttribute,
    handleDeleteAttribute,
    handleSaveAttributeLayout,
    handleDeleteAttributeLayout,
  };
});

export default useAttributeApi(pinia);
