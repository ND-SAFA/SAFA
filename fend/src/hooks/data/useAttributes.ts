import { defineStore } from "pinia";

import { AttributeLayoutSchema, AttributeSchema, ProjectSchema } from "@/types";
import { removeMatches } from "@/util";
import { pinia } from "@/plugins";

/**
 * This module defines the state of artifact attributes and their layouts.
 */
export const useAttributes = defineStore("attributes", {
  state: () => ({
    /**
     * A list of custom attributes used on this project.
     */
    attributes: [] as AttributeSchema[],
    /**
     * Layouts for displaying this project's custom attributes.
     */
    attributeLayouts: [] as AttributeLayoutSchema[],
    /**
     * The id of the current layout selected for editing.
     */
    selectedLayoutId: "",
  }),
  getters: {
    /**
     * The first layout with empty artifact types will be used as the default for all artifacts.
     *
     * @return The default layout for artifact attributes.
     */
    defaultLayout(): AttributeLayoutSchema | undefined {
      return this.attributeLayouts.find(
        ({ artifactTypes }) => artifactTypes.length === 0
      );
    },
  },
  actions: {
    /**
     * Initializes the current project.
     */
    initializeProject(project: ProjectSchema): void {
      this.attributes = project.attributes || [];
      this.attributeLayouts = project.attributeLayouts || [];
      this.selectedLayoutId = project.attributeLayouts?.[0]?.id || "";
    },

    /**
     * Updates the stored custom attributes.
     *
     * @param updatedAttributes - The updated attributes.
     */
    updateAttributes(updatedAttributes: AttributeSchema[]): void {
      const ids = updatedAttributes.map(({ key }) => key);

      this.attributes = [
        ...removeMatches(this.attributes, "key", ids),
        ...updatedAttributes,
      ];
    },
    /**
     * Deletes from the stored custom attributes.
     *
     * @param deletedAttributes - The keys of attributes to delete.
     */
    deleteAttributes(deletedAttributes: string[]): void {
      this.attributes = removeMatches(
        this.attributes,
        "key",
        deletedAttributes
      );
    },

    /**
     * Updates the stored custom attribute layouts.
     *
     * @param updatedLayouts - The updated layouts.
     */
    updateAttributeLayouts(updatedLayouts: AttributeLayoutSchema[]): void {
      const ids = updatedLayouts.map(({ id }) => id);

      this.attributeLayouts = [
        ...removeMatches(this.attributeLayouts, "id", ids),
        ...updatedLayouts,
      ];
    },
    /**
     * Deletes from the stored custom attribute layouts.
     *
     * @param deletedLayouts - The ids of layouts to delete.
     */
    deleteAttributeLayouts(deletedLayouts: string[]): void {
      this.attributeLayouts = removeMatches(
        this.attributeLayouts,
        "id",
        deletedLayouts
      );
    },
    /**
     * Returns the attribute grid layout for the given artifact type.
     *
     * @param type - The type to find.
     * @return The attribute layout.
     */
    getLayoutByType(type: string): AttributeLayoutSchema | undefined {
      return (
        this.attributeLayouts.find(({ artifactTypes }) =>
          artifactTypes.includes(type)
        ) || this.defaultLayout
      );
    },
    /**
     * Adds or updates an attribute.
     * @param attribute - The attribute to add.
     */
    updateAttribute(attribute: AttributeSchema): void {
      const existingIndex = this.attributes.findIndex(
        ({ key }) => key === attribute.key
      );

      if (existingIndex === -1) {
        this.attributes.push(attribute);
      } else {
        this.attributes.splice(existingIndex, 1, attribute);
      }
    },
    /**
     * Deletes an attribute.
     * @param attribute - The attribute to delete.
     */
    deleteAttribute(attribute: AttributeSchema): void {
      this.attributes = this.attributes.filter(
        ({ key }) => key !== attribute.key
      );
    },
    /**
     * Adds or updates an attribute layout.
     * @param layout - The attribute layout to add.
     */
    updateLayout(layout: AttributeLayoutSchema): void {
      const existingIndex = this.attributeLayouts.findIndex(
        ({ id }) => id === layout.id
      );

      if (existingIndex === -1) {
        this.attributeLayouts.push(layout);
      } else {
        this.attributeLayouts.splice(existingIndex, 1, layout);
      }
    },
    /**
     * Deletes an attribute layout.
     * @param layout - The attribute layout to delete.
     */
    deleteLayout(layout: AttributeLayoutSchema): void {
      this.attributeLayouts = this.attributeLayouts.filter(
        ({ id }) => id !== layout.id
      );

      if (this.selectedLayoutId !== layout.id) return;

      this.selectedLayoutId = this.attributeLayouts[0]?.id || "";
    },
  },
});

export default useAttributes(pinia);
