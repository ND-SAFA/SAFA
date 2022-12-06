import { defineStore } from "pinia";

import { GenerationModelSchema } from "@/types";
import { createModel } from "@/util";
import { pinia } from "@/plugins";

/**
 * The save model store assists in creating and editing project models.
 */
export const useSaveModel = defineStore("saveModel", {
  state: () => ({
    /**
     * A base model being edited.
     */
    baseModel: undefined as GenerationModelSchema | undefined,
    /**
     * The model being created or edited.
     */
    editedModel: createModel(),
  }),
  getters: {
    /**
     * @return Whether an existing model is being updated.
     */
    isUpdate(): boolean {
      return !!this.baseModel;
    },
    /**
     * @return Whether the model can be saved.
     */
    canSave(): boolean {
      return this.editedModel.name.length > 0;
    },
  },
  actions: {
    /**
     * Resets the model value to the given base value.
     */
    resetModel(): void {
      this.editedModel = createModel(this.baseModel);
    },
  },
});

export default useSaveModel(pinia);
