import { defineStore } from "pinia";

import { ArtifactSchema } from "@/types";
import { appStore, traceStore } from "@/hooks";
import { pinia } from "@/plugins";
import artifactStore from "../project/useArtifacts";

/**
 * The save trace store assists in creating batches of trace links.
 */
export const useSaveTrace = defineStore("saveTrace", {
  state: () => ({
    /**
     * The source artifact ids.
     */
    sourceIds: null as string[] | null,
    /**
     * The target artifact ids.
     */
    targetIds: null as string[] | null,
  }),
  getters: {
    /**
     * @return The number of source artifacts.
     */
    sourceCount(): number {
      return this.sourceIds?.length || 0;
    },
    /**
     * @return The number of target artifacts.
     */
    targetCount(): number {
      return this.targetIds?.length || 0;
    },
    /**
     * @return The source artifacts.
     */
    sources(): (ArtifactSchema | undefined)[] {
      return (
        this.sourceIds?.map((id) => artifactStore.getArtifactById(id)) || []
      );
    },
    /**
     * @return The target artifacts.
     */
    targets(): (ArtifactSchema | undefined)[] {
      return (
        this.targetIds?.map((id) => artifactStore.getArtifactById(id)) || []
      );
    },
    /**
     * @return If the source and target ids are valid, returns empty, else returns an error message.
     */
    errorMessage(): string {
      if (this.sourceCount > 1 && this.targetCount > 1) {
        return "Cannot create a trace link between multiple source and multiple target artifacts.";
      }

      for (const target of this.targets) {
        for (const source of this.sources) {
          if (!source) {
            return "Source artifact does not exist.";
          } else if (!target) {
            return "Target artifact does not exist.";
          }

          const isLinkAllowed = traceStore.isLinkAllowed(source, target);

          if (isLinkAllowed !== true) {
            return isLinkAllowed || "Cannot create a trace link.";
          }
        }
      }

      return "";
    },
    /**
     * @return Whether the links to be created are valid and can be saved.
     */
    canSave(): boolean {
      return this.sourceCount > 0 && this.targetCount > 0 && !this.errorMessage;
    },
  },
  actions: {
    /**
     * Resets the state of the trace based on selected artifacts.
     */
    resetTrace(): void {
      const openState = appStore.isTraceCreatorOpen;

      this.sourceIds = [];
      this.targetIds = [];

      if (typeof openState !== "object") return;

      if (openState.type === "source") {
        this.sourceIds = [openState.artifactId];
      } else if (openState.type === "target") {
        this.targetIds = [openState.artifactId];
      } else {
        this.sourceIds = [openState.sourceId];
        this.targetIds = [openState.targetId];
      }
    },
  },
});

export default useSaveTrace(pinia);
