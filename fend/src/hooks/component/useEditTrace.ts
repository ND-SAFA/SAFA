import { defineStore } from "pinia";

import { TraceLinkSchema } from "@/types";
import { buildTraceLink } from "@/util";
import { appStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * The edit trace link store assists in editing trace links.
 */
export const useEditTrace = defineStore("editTrace", {
  state: () => ({
    /**
     * A base trace link being edited.
     */
    baseTrace: undefined as TraceLinkSchema | undefined,
    /**
     * The trace link being created or edited.
     */
    editedTrace: buildTraceLink(),
  }),
  getters: {
    /**
     * @return Whether an existing trace link is being updated.
     */
    isUpdate(): boolean {
      return !!this.baseTrace;
    },
  },
  actions: {
    /**
     * Resets the trace link value to the given base value.
     */
    resetTrace(trace?: TraceLinkSchema): void {
      if (trace) {
        this.baseTrace = trace;
      }

      this.editedTrace = buildTraceLink(this.baseTrace);
    },
    /**
     * Opens the edit trace link panel.
     * @param trace - The trace link to edit.
     */
    openPanel(trace?: TraceLinkSchema): void {
      this.resetTrace(trace);
      appStore.openDetailsPanel("editTrace");
    },
  },
});

export default useEditTrace(pinia);
