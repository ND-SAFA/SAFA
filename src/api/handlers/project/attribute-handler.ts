import { AttributeLayoutSchema, AttributeSchema } from "@/types";
import { attributesStore } from "@/hooks";

export default {};

/**
 * Creates or edits an attribute and updates the store.
 * @param attribute - The attribute to save.
 */
export function handleSaveAttribute(attribute: AttributeSchema): void {
  //TODO: update api and store, log status

  //TODO: use returned attribute.
  attributesStore.updateAttribute(attribute);
}

/**
 * Deletes an attribute and updates the store.
 * @param attribute - The attribute to delete.
 */
export function handleDeleteAttribute(attribute: AttributeSchema): void {
  //TODO: update api and store, log status

  attributesStore.deleteAttribute(attribute);
}

/**
 * Creates or edits an attribute layout and updates the store.
 * @param layout - The attribute layout to save.
 */
export function handleSaveAttributeLayout(layout: AttributeLayoutSchema): void {
  //TODO: update api and store, log status

  //TODO: use returned layout.
  attributesStore.updateLayout(layout);
}

/**
 * Deletes an attribute layout layout and updates the store.
 * @param layout - The attribute layout to delete.
 */
export function handleDeleteAttributeLayout(
  layout: AttributeLayoutSchema
): void {
  //TODO: update api and store, log status

  attributesStore.deleteLayout(layout);
}
