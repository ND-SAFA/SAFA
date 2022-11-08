<template>
  <div v-if="isOpen" data-cy="panel-trace-save">
    <artifact-input
      v-model="sourceArtifactId"
      label="Source Artifact"
      :multiple="false"
      data-cy="button-trace-save-source"
      class="my-4"
    />
    <artifact-input
      v-model="targetArtifactId"
      label="Target Artifact"
      :multiple="false"
      data-cy="button-trace-save-target"
      class="my-4"
    />

    <v-expansion-panels>
      <v-expansion-panel data-cy="panel-trace-directions">
        <v-expansion-panel-header>
          <typography value="Allowed Trace Directions" />
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <div v-for="entry in typeDirections" :key="entry.label">
            <type-direction-input :entry="entry" />
          </div>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>

    <v-divider class="my-4" />
    <flex-box justify="space-between" align="center">
      <typography color="error" r="2" :value="errorMessage" />
      <v-btn
        color="primary"
        :disabled="!canSave"
        data-cy="button-trace-save"
        @click="handleSubmit"
      >
        Create
      </v-btn>
    </flex-box>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactModel, LabelledTraceDirectionModel } from "@/types";
import { appStore, artifactStore, traceStore, typeOptionsStore } from "@/hooks";
import { handleCreateLink } from "@/api";
import {
  Typography,
  ArtifactInput,
  TypeDirectionInput,
  FlexBox,
} from "@/components/common";

/**
 * Allows for creating trace links.
 */
export default Vue.extend({
  name: "SaveTraceLinkPanel",
  components: { FlexBox, Typography, ArtifactInput, TypeDirectionInput },
  data() {
    return {
      sourceArtifactId: "",
      targetArtifactId: "",
    };
  },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "saveTrace";
    },

    /**
     * @return The source artifact.
     */
    sourceArtifact(): ArtifactModel | undefined {
      return artifactStore.getArtifactById(this.sourceArtifactId);
    },
    /**
     * @return The source artifact.
     */
    targetArtifact(): ArtifactModel | undefined {
      return artifactStore.getArtifactById(this.targetArtifactId);
    },
    /**
     * @return Any errors in trying to create this link.
     */
    errorMessage(): string {
      const source = this.sourceArtifact;
      const target = this.targetArtifact;

      if (!source || !target) return "";

      const isLinkAllowed = traceStore.isLinkAllowed(source, target);

      return isLinkAllowed === true
        ? ""
        : isLinkAllowed || "Cannot create a trace link.";
    },
    /**
     * @return Whether a link can be created.
     */
    canSave(): boolean {
      return (
        !!this.sourceArtifactId &&
        !!this.targetArtifactId &&
        this.errorMessage === ""
      );
    },
    /**
     * @return The current project's artifact types.
     */
    typeDirections(): LabelledTraceDirectionModel[] {
      return typeOptionsStore.typeDirections();
    },
  },
  methods: {
    /**
     * Creates a trace link from the given artifacts.
     */
    async handleSubmit(): Promise<void> {
      const source = this.sourceArtifact;
      const target = this.targetArtifact;

      if (!source || !target) return;

      await handleCreateLink(source, target);
      this.handleClose();
    },
    /**
     * Closes the trace link creator.
     */
    handleClose(): void {
      appStore.closeSidePanels();
    },
  },
  watch: {
    /**
     * Resets fields when the panel opens.
     */
    isOpen(open: boolean) {
      if (!open) return;

      this.sourceArtifactId = "";
      this.targetArtifactId = "";
    },
  },
});
</script>
