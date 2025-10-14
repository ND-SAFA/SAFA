import { defineStore } from "pinia";

import { AttributeLayoutSchema, AttributeSchema } from "@/types";
import { buildAttributeLayout, DEFAULT_LAYOUT_ID } from "@/util";
import { attributesStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * The save attribute store assists in creating and editing attribute layouts.
 */
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSaveAttributeLayout = (id: string) =>
  defineStore(`saveAttributeLayout-${id}`, {
    state: () => ({
      /**
       * The stored base attribute layout being edited.
       */
      baseLayout: undefined as AttributeLayoutSchema | undefined,
      /**
       * The attribute layout being created or edited.
       */
      editedLayout: buildAttributeLayout(),
    }),
    getters: {
      /**
       * @return Whether the current layout is not the default one.
       */
      isCustom(): boolean {
        return this.baseLayout?.id !== DEFAULT_LAYOUT_ID;
      },
      /**
       * @return Whether an existing attribute layout is being updated.
       */
      isUpdate(): boolean {
        return !!this.baseLayout;
      },
      /**
       * @return An error if this layout's list of types overlaps with another layout.
       */
      typeErrors(): string | undefined {
        const { artifactTypes, id } = this.editedLayout;

        for (const layout of attributesStore.attributeLayouts || []) {
          if (layout.id === id) continue;

          if (artifactTypes.length === 0 && layout.artifactTypes.length === 0) {
            return `A default layout already exists: ${layout.name}.`;
          }

          for (const type of artifactTypes) {
            if (layout.artifactTypes.includes(type)) {
              return `A layout for "${type}" already exists: ${layout.name}.`;
            }
          }
        }
      },
      /**
       * @return Whether this attribute layout can be saved.
       */
      canSave(): boolean {
        return !!this.editedLayout.name && !this.typeErrors;
      },
    },
    actions: {
      /**
       * Resets the state of the attribute layout to the selected artifact.
       * @param baseLayout - The layout to reset data to.
       */
      resetLayout(baseLayout: AttributeLayoutSchema | undefined): void {
        this.baseLayout = baseLayout;
        this.editedLayout = buildAttributeLayout(this.baseLayout);
      },
      /**
       * Adds an attribute to the bottom of the edited layout.
       * @param key - The attribute key to add to the layout.
       */
      addAttribute(key: string): void {
        const y =
          this.editedLayout.positions.length === 0
            ? 0
            : Math.max(0, ...this.editedLayout.positions.map(({ y }) => y)) + 1;

        this.editedLayout.positions.push({
          key,
          y,
          x: 0,
          width: 1,
          height: 1,
        });
      },
      /**
       * Removes an attribute from the layout.
       * @param attribute - The attribute to add to the layout.
       */
      deleteAttribute(attribute: AttributeSchema): void {
        this.editedLayout.positions = this.editedLayout.positions.filter(
          ({ key }) => key !== attribute.key
        );
      },
    },
  });

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export default (id: string) => useSaveAttributeLayout(id)(pinia);
