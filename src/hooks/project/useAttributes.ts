import { defineStore } from "pinia";

import {
  AttributeLayoutModel,
  AttributeModel,
  AttributePositionModel,
  ProjectModel,
} from "@/types";
import { removeMatches } from "@/util";
import { projectStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * This module defines the state of artifact attributes and their layouts.
 */
export const useAttributes = defineStore("attributes", {
  state: () => ({
    /**
     * A list of custom attributes used on this project.
     */
    attributes: [] as AttributeModel[],
    /**
     * Layouts for displaying this project's custom attributes.
     */
    attributeLayouts: [] as AttributeLayoutModel[],
  }),
  getters: {
    /**
     * The first layout with empty artifact types will be used as the default for all artifacts.
     *
     * @return The default layout for artifact attributes.
     */
    defaultLayout(): AttributePositionModel[] {
      const layout = this.attributeLayouts.find(
        ({ artifactTypes }) => artifactTypes.length === 0
      );

      return layout?.positions || [];
    },
  },
  actions: {
    /**
     * Initializes the current project.
     */
    initializeProject(project: ProjectModel): void {
      this.attributes = project.attributes || [];
      this.attributeLayouts = project.attributeLayouts || [];
    },

    /**
     * Updates the stored custom attributes.
     *
     * @param updatedAttributes - The updated attributes.
     */
    updateAttributes(updatedAttributes: AttributeModel[]): void {
      const ids = updatedAttributes.map(({ key }) => key);

      this.attributes = [
        ...removeMatches(this.attributes, "key", ids),
        ...updatedAttributes,
      ];

      projectStore.project.attributes = this.attributes;
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

      projectStore.project.attributes = this.attributes;
    },

    /**
     * Updates the stored custom attribute layouts.
     *
     * @param updatedLayouts - The updated layouts.
     */
    updateAttributeLayouts(updatedLayouts: AttributeLayoutModel[]): void {
      const ids = updatedLayouts.map(({ id }) => id);

      this.attributeLayouts = [
        ...removeMatches(this.attributeLayouts, "id", ids),
        ...updatedLayouts,
      ];

      projectStore.project.attributeLayouts = this.attributeLayouts;
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

      projectStore.project.attributeLayouts = this.attributeLayouts;
    },
  },
});

export default useAttributes(pinia);
