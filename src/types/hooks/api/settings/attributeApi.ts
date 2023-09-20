import {
  AttributeLayoutSchema,
  AttributeSchema,
  IOHandlerCallback,
} from "@/types";

/**
 * A hook for calling artifact custom attribute API endpoints.
 */
export interface AttributeApiHook {
  /**
   * Creates or edits an attribute and updates the store.
   *
   * @param attribute - The attribute to save.
   * @param isUpdate - Whether an existing attribute is being updated.
   * @param callbacks - Callbacks to call after the action.
   */
  handleSaveAttribute(
    attribute: AttributeSchema,
    isUpdate: boolean,
    callbacks?: IOHandlerCallback
  ): Promise<void>;
  /**
   * Deletes an attribute and updates the store.
   *
   * @param attribute - The attribute to delete.
   * @param callbacks - Callbacks to call after the action.
   */
  handleDeleteAttribute(
    attribute: AttributeSchema,
    callbacks?: IOHandlerCallback
  ): Promise<void>;
  /**
   * Creates or edits an attribute layout and updates the store.
   *
   * @param layout - The attribute layout to save.
   * @param isUpdate - Whether an existing attribute layout is being updated.
   * @param callbacks - Callbacks to call after the action.
   */
  handleSaveAttributeLayout(
    layout: AttributeLayoutSchema,
    isUpdate: boolean,
    callbacks?: IOHandlerCallback<AttributeLayoutSchema>
  ): Promise<void>;
  /**
   * Deletes an attribute layout and updates the store.
   *
   * @param layout - The attribute layout to delete.
   * @param callbacks - Callbacks to call after the action.
   */
  handleDeleteAttributeLayout(
    layout: AttributeLayoutSchema,
    callbacks?: IOHandlerCallback
  ): Promise<void>;
}
