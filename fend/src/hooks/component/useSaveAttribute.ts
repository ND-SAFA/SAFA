import { defineStore } from "pinia";

import { AttributeSchema, AttributeType } from "@/types";
import { buildAttribute } from "@/util";
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
      editedAttribute: buildAttribute(),
    }),
    getters: {
      /**
       * @return Whether an existing attribute is being updated.
       */
      isUpdate(): boolean {
        return !!this.baseAttribute;
      },
      /**
       * @return Whether this attribute can be edited.
       */
      isReadOnly(): boolean {
        return this.baseAttribute?.key.startsWith("~") || false;
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
        return ["select", "multiselect"].includes(this.type);
      },
      /**
       * @return Whether this attribute value has min and max bounds.
       */
      showBounds(): boolean {
        return ["text", "paragraph", "int", "float"].includes(this.type);
      },
      /**
       * @return The hint for the min bound.
       */
      minBoundHint(): string {
        return ["int", "float"].includes(this.type)
          ? "The minimum value of this number."
          : "The minimum length of this value.";
      },
      /**
       * @return The hint for the max bound.
       */
      maxBoundHint(): string {
        return ["int", "float"].includes(this.type)
          ? "The maximum value of this number."
          : "The maximum length of this value.";
      },
      /**
       * @return The error message for the key.
       */
      keyError(): string {
        return this.editedAttribute.key.startsWith("~")
          ? "Key cannot start with ~"
          : "";
      },
      /**
       * @return Whether this attribute can be saved.
       */
      canSave(): boolean {
        return (
          !!this.editedAttribute.key &&
          !!this.editedAttribute.label &&
          !!this.editedAttribute.type &&
          !this.keyError
        );
      },
    },
    actions: {
      /**
       * Resets the state of the attribute to the selected artifact.
       */
      resetAttribute(baseAttribute: AttributeSchema | undefined): void {
        this.baseAttribute = baseAttribute;
        this.editedAttribute = buildAttribute(this.baseAttribute);
      },
    },
  });

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export default (id: string) => useSaveAttribute(id)(pinia);
