import { defineStore } from "pinia";

import { ArtifactSchema, TraceCreatorOpenState } from "@/types";
import {
  subtreeStore,
  timStore,
  traceStore,
  artifactStore,
  appStore,
} from "@/hooks";
import { pinia } from "@/plugins";

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
    /**
     * The trace link explanation.
     */
    explanation: "",
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
     * @return The default artifact types hidden from source artifacts.
     * - If source artifacts are set, the default filter will be set to their types.
     * - If target artifacts are set, the default filter will be set to the types
     *   of the source artifacts that can be linked to the target artifacts.
     * - If neither are set, the default filter will be set to all types.
     */
    defaultHiddenSourceTypes(): string[] {
      const allTypes = timStore.typeNames;
      let hiddenTypes: string[] = [];

      if (this.sourceCount > 0) {
        const sourceTypes = this.sources
          .map((source) => source?.type || "")
          .filter((type) => !!type);

        hiddenTypes = allTypes.filter((type) => !sourceTypes.includes(type));
      } else if (this.targetCount > 0) {
        const targetTypes = this.targets
          .map((target) => target?.type || "")
          .filter((type) => !!type);
        const sourceTypes = timStore.traceMatrices
          .map((matrix) =>
            targetTypes.includes(matrix.targetType) ? matrix.sourceType : ""
          )
          .filter((type) => !!type);

        hiddenTypes = allTypes.filter((type) => !sourceTypes.includes(type));
      }

      if (hiddenTypes.length === allTypes.length) {
        hiddenTypes = [];
      }

      return hiddenTypes;
    },
    /**
     * @return The default artifact types hidden from target artifacts.
     * - If target artifacts are set, the default filter will be set to their types.
     * - If source artifacts are set, the default filter will be set to the types
     *   of the target artifacts that can be linked to the source artifacts.
     * - If neither are set, the default filter will be set to all types.
     */
    defaultHiddenTargetTypes(): string[] {
      const allTypes = timStore.typeNames;
      let hiddenTypes: string[] = [];

      if (this.targetCount > 0) {
        const targetTypes = this.targets
          .map((target) => target?.type || "")
          .filter((type) => !!type);

        hiddenTypes = allTypes.filter((type) => !targetTypes.includes(type));
      } else if (this.sourceCount > 0) {
        const sourceTypes = this.sources
          .map((source) => source?.type || "")
          .filter((type) => !!type);
        const targetTypes = timStore.traceMatrices
          .map((matrix) =>
            sourceTypes.includes(matrix.sourceType) ? matrix.targetType : ""
          )
          .filter((type) => !!type);

        hiddenTypes = allTypes.filter((type) => !targetTypes.includes(type));
      }

      if (hiddenTypes.length === allTypes.length) {
        hiddenTypes = [];
      }

      return hiddenTypes;
    },
    /**
     * @return The default artifact ids hidden from target artifacts,
     * as they are already traced to source artifacts.
     */
    hiddenTargetIds(): string[] {
      if (this.sourceCount === 0) return [];

      return (this.sourceIds || [])
        .map((id) => subtreeStore.getSubtreeItem(id).parents)
        .reduce((acc, cur) => [...acc, ...cur], []);
    },
    /**
     * @return The default artifact ids hidden from source artifacts,
     * as they are already traced to target artifacts.
     */
    hiddenSourceIds(): string[] {
      if (this.targetCount === 0) return [];

      return (this.targetIds || [])
        .map((id) => subtreeStore.getSubtreeItem(id).children)
        .reduce((acc, cur) => [...acc, ...cur], []);
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
            return "Child artifact does not exist.";
          } else if (!target) {
            return "Parent artifact does not exist.";
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
    resetTrace(openTo?: TraceCreatorOpenState): void {
      this.sourceIds = [];
      this.targetIds = [];
      this.explanation = "";

      if (typeof openTo !== "object") return;

      if (openTo.type === "source") {
        this.sourceIds = [openTo.artifactId];
      } else if (openTo.type === "target") {
        this.targetIds = [openTo.artifactId];
      } else {
        this.sourceIds = openTo.sourceIds;
        this.targetIds = openTo.targetIds;
      }
    },
    /**
     * Opens the trace creator to a specific source and target artifacts.
     *
     * @param openTo - What to open to.
     */
    openPanel(openTo?: TraceCreatorOpenState): void {
      this.resetTrace(openTo);
      appStore.openDetailsPanel("saveTrace");
    },
  },
});

export default useSaveTrace(pinia);
