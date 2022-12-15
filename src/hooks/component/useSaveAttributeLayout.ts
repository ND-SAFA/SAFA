import { defineStore } from "pinia";

import { AttributeLayoutSchema } from "@/types";
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
       */
      resetLayout(baseLayout: AttributeLayoutSchema): void {
        this.baseLayout = baseLayout;
        this.editedLayout = createAttributeLayout(this.baseLayout);
      },
    },
  });

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export default (id: string) => useSaveAttributeLayout(id)(pinia);
