import { defineStore } from "pinia";

import {
  AttributeApiHook,
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

/**
 * A hook for managing artifact custom attribute API requests.
 */
export const useAttributeApi = defineStore(
  "attributeApi",
  (): AttributeApiHook => {
    const attributeApi = useApi("attributeApi");
    const attributeLayoutApi = useApi("attributeLayoutApi");

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
            const createdAttribute = await createAttribute(
              projectId,
              attribute
            );

            attributesStore.updateAttribute(createdAttribute);
          }
        },
        {
          ...callbacks,
          success: isUpdate
            ? `Edited attribute: ${attribute.label}`
            : `Created attribute: ${attribute.label}`,
          error: `Unable to save attribute: ${attribute.label}`,
        }
      );
    }

    async function handleDeleteAttribute(
      attribute: AttributeSchema,
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      logStore.confirm(
        "Delete Attribute",
        `Are you sure you would like to delete "${attribute.label}"?`,
        async (isConfirmed: boolean) => {
          if (!isConfirmed) return;

          await attributeApi.handleRequest(
            async () => {
              await deleteAttribute(projectStore.projectId, attribute);

              attributesStore.deleteAttribute(attribute);
            },
            {
              ...callbacks,
              success: `Deleted attribute: ${attribute.label}`,
              error: `Unable to delete attribute: ${attribute.label}`,
            }
          );
        }
      );
    }

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
        {
          ...callbacks,
          success: isUpdate
            ? `Edited attribute layout: ${layout.name}`
            : `Created attribute layout: ${layout.name}`,
          error: `Unable to save attribute layout: ${layout.name}`,
        }
      );
    }

    async function handleDeleteAttributeLayout(
      layout: AttributeLayoutSchema,
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      logStore.confirm(
        "Delete Attribute Layout",
        `Are you sure you would like to delete "${layout.name}"?`,
        async (isConfirmed: boolean) => {
          if (!isConfirmed) return;

          await attributeLayoutApi.handleRequest(
            async () => {
              await deleteAttributeLayout(projectStore.projectId, layout);

              attributesStore.deleteLayout(layout);
            },
            {
              ...callbacks,
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
  }
);

export default useAttributeApi(pinia);
