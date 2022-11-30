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
     *
     * TODO: remove testing values.
     */
    initializeProject(project: ProjectModel): void {
      this.attributes = project.attributes || [
        {
          key: "str",
          label: "Custom String",
          type: "text",
          min: 4,
          max: 4,
        },
        {
          key: "int",
          label: "Custom Int",
          type: "int",
          min: 0,
          max: 5,
        },
        {
          key: "sel",
          label: "Custom Select",
          type: "select",
          options: ["A", "B", "C"],
        },
        {
          key: "multi",
          label: "Custom Multiselect",
          type: "multiselect",
          options: ["A", "B", "C"],
          min: 1,
          max: 2,
        },
        {
          key: "date",
          label: "Custom Date",
          type: "date",
        },
        {
          key: "float",
          label: "Custom Float",
          type: "float",
        },
        {
          key: "bool",
          label: "Custom Boolean",
          type: "boolean",
        },
        {
          key: "rel",
          label: "Custom Relation",
          type: "relation",
        },
        {
          key: "par",
          label: "Custom Paragraph",
          type: "paragraph",
        },
      ];
      this.attributeLayouts = project.attributeLayouts || [
        {
          id: "default",
          artifactTypes: [],
          positions: [
            { x: 0, y: 0, width: 1, height: 1, key: "str" },
            { x: 1, y: 0, width: 1, height: 1, key: "bool" },

            { x: 0, y: 1, width: 1, height: 1, key: "date" },

            { x: 0, y: 2, width: 1, height: 1, key: "int" },
            { x: 1, y: 2, width: 1, height: 1, key: "float" },

            { x: 0, y: 3, width: 1, height: 1, key: "sel" },
            { x: 1, y: 3, width: 1, height: 1, key: "rel" },

            { x: 0, y: 4, width: 2, height: 1, key: "multi" },

            { x: 0, y: 5, width: 2, height: 1, key: "par" },
          ],
        },
      ];
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
