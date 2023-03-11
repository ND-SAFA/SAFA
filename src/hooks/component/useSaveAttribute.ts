import { defineStore } from "pinia";

import { AttributeSchema, AttributeType } from "@/types";
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
       * @return The data type of this attribute.
       */
      type(): AttributeType {
        return this.editedAttribute.type;
      },
      /**
       * @return Whether this attribute value has selectable options.
       */
      showOptions(): boolean {
        return [AttributeType.select, AttributeType.multiselect].includes(
          this.type
        );
      },
      /**
       * @return Whether this attribute value has min and max bounds.
       */
      showBounds(): boolean {
        return [
          AttributeType.text,
          AttributeType.paragraph,
          AttributeType.int,
          AttributeType.float,
        ].includes(this.type);
      },
      /**
       * @return The hint for the min bound.
       */
      minBoundHint(): string {
        return [AttributeType.int, AttributeType.float].includes(this.type)
          ? "The minimum value of this number."
          : "The minimum length of this value.";
      },
      /**
       * @return The hint for the max bound.
       */
      maxBoundHint(): string {
        return [AttributeType.int, AttributeType.float].includes(this.type)
          ? "The maximum value of this number."
          : "The maximum length of this value.";
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
      resetAttribute(baseAttribute: AttributeSchema | undefined): void {
        this.baseAttribute = baseAttribute;
        this.editedAttribute = createAttribute(this.baseAttribute);
      },
    },
  });

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export default (id: string) => useSaveAttribute(id)(pinia);
