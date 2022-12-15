import { defineStore } from "pinia";

import { AttributeLayoutSchema, AttributeSchema } from "@/types";
import { createAttributeLayout } from "@/util";
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
      editedLayout: createAttributeLayout(),
    }),
    getters: {
      /**
       * @return Whether the current layout is not the default one.
       */
      isCustom(): boolean {
        return this.baseLayout?.id !== "default";
      },
      /**
       * @return Whether an existing attribute layout is being updated.
       */
      isUpdate(): boolean {
        return !!this.baseLayout;
      },
      /**
       * @return Whether this attribute layout can be saved.
       */
      canSave(): boolean {
        return !!this.editedLayout.name;
      },
    },
    actions: {
      /**
       * Resets the state of the attribute layout to the selected artifact.
       * @param baseLayout - The layout to reset data to.
       */
      resetLayout(baseLayout: AttributeLayoutSchema): void {
        this.baseLayout = baseLayout;
        this.editedLayout = createAttributeLayout(this.baseLayout);
      },
      /**
       * Adds an attribute to the bottom of the edited layout.
       * @param key - The attribute key to add to the layout.
       */
      addAttribute(key: string): void {
        const y =
          Math.max(...this.editedLayout.positions.map(({ y }) => y)) + 1;

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
