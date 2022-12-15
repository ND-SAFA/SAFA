import { defineStore } from "pinia";

import { AttributeSchema } from "@/types";
import { createAttribute } from "@/util";
import { pinia } from "@/plugins";

/**
 * The save attribute store assists in creating and editing attributes.
 */
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSaveAttribute = (id: string) =>
  defineStore(`saveAttribute-${id}`, {
    state: () => ({
      /**
       * The stored base attribute being edited.
       */
      baseAttribute: undefined as AttributeSchema | undefined,
      /**
       * The attribute being created or edited.
       */
      editedAttribute: createAttribute(),
    }),
    getters: {
      /**
       * @return Whether an existing attribute is being updated.
       */
      isUpdate(): boolean {
        return !!this.baseAttribute;
      },
      /**
       * @return Whether this attribute can be saved.
       */
      canSave(): boolean {
        return (
          !!this.editedAttribute.key &&
          !!this.editedAttribute.label &&
          !!this.editedAttribute.type
        );
      },
    },
    actions: {
      /**
       * Resets the state of the attribute to the selected artifact.
       */
      resetAttribute(baseAttribute: AttributeSchema): void {
        this.baseAttribute = baseAttribute;
        this.editedAttribute = createAttribute(this.baseAttribute);
      },
    },
  });

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export default (id: string) => useSaveAttribute(id)(pinia);
