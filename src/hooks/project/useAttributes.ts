import { defineStore } from "pinia";

import {
  AttributeLayoutSchema,
  AttributePositionSchema,
  AttributeSchema,
  AttributeType,
  ProjectSchema,
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
    attributes: [] as AttributeSchema[],
    /**
     * Layouts for displaying this project's custom attributes.
     */
    attributeLayouts: [] as AttributeLayoutSchema[],
    /**
     * The index of the current layout selected for editing.
     */
    selectedLayout: 0,
  }),
  getters: {
    /**
     * The first layout with empty artifact types will be used as the default for all artifacts.
     *
     * @return The default layout for artifact attributes.
     */
    defaultLayout(): AttributePositionSchema[] {
      const layout = this.attributeLayouts.find(
        ({ artifactTypes }) => artifactTypes.length === 0
      );

      return layout?.positions || [];
    },
    /**
     * @return The id of the selected layout.
     */
    selectedLayoutId(): string {
      return this.attributeLayouts[this.selectedLayout]?.id || "";
    },
  },
  actions: {
    /**
     * Initializes the current project.
     */
    initializeProject(project: ProjectSchema): void {
      this.attributes =
        project.attributes ||
        [
          // {
          //   key: "1",
          //   label: "Paragraph",
          //   type: AttributeType.paragraph,
          // },
          // {
          //   key: "2",
          //   label: "Relation",
          //   type: AttributeType.relation,
          // },
          // {
          //   key: "3",
          //   label: "Boolean",
          //   type: AttributeType.boolean,
          // },
          // {
          //   key: "4",
          //   label: "Multiselect",
          //   type: AttributeType.multiselect,
          //   options: [
          //     "One option",
          //     "Another option",
          //     "And another option",
          //     "And one more",
          //   ],
          // },
          // {
          //   key: "5",
          //   label: "Number",
          //   type: AttributeType.float,
          //   max: 5,
          //   min: 1,
          // },
        ];
      this.attributeLayouts =
        project.attributeLayouts ||
        [
          // {
          //   id: "2",
          //   name: "Default",
          //   artifactTypes: [],
          //   positions: [
          //     {
          //       x: 0,
          //       y: 0,
          //       width: 1,
          //       height: 1,
          //       key: "1",
          //     },
          //     {
          //       x: 0,
          //       y: 1,
          //       width: 1,
          //       height: 1,
          //       key: "3",
          //     },
          //     {
          //       x: 1,
          //       y: 1,
          //       width: 1,
          //       height: 1,
          //       key: "2",
          //     },
          //     {
          //       x: 0,
          //       y: 2,
          //       width: 1,
          //       height: 1,
          //       key: "4",
          //     },
          //     {
          //       x: 0,
          //       y: 3,
          //       width: 1,
          //       height: 1,
          //       key: "5",
          //     },
          //   ],
          // },
        ];
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
    updateAttributeLayouts(updatedLayouts: AttributeLayoutSchema[]): void {
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
    /**
     * Returns the layout based on an artifact type.
     *
     * @param type - The type to find.
     * @return The attribute layout.
     */
    getLayoutByType(type: string): AttributeLayoutSchema {
      return (
        this.attributeLayouts.find(({ artifactTypes }) =>
          artifactTypes.includes(type)
        ) || this.attributeLayouts[0]
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
    },
  },
});

export default useAttributes(pinia);
