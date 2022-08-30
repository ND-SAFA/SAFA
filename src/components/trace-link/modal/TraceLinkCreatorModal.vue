<template>
  <generic-modal
    title="Create Trace Link"
    :is-open="isOpen"
    @close="$emit('close')"
    size="l"
    data-cy="modal-trace-save"
  >
    <template v-slot:body>
      <v-row class="my-2">
        <v-col cols="6">
          <artifact-input
            v-model="sourceArtifactId"
            label="Source Artifact"
            :multiple="false"
            data-cy="button-trace-save-source"
          />
        </v-col>
        <v-col cols="6">
          <artifact-input
            v-model="targetArtifactId"
            label="Target Artifact"
            :multiple="false"
            data-cy="button-trace-save-target"
          />
        </v-col>
      </v-row>
      <v-expansion-panels flat>
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
    </template>
    <template v-slot:actions>
      <v-spacer />
      <typography color="error" r="2" :value="errorMessage" />
      <v-btn
        color="primary"
        :disabled="!canSave"
        data-cy="button-trace-save"
        @click="handleSubmit"
      >
        Create
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactModel, LabelledTraceDirectionModel } from "@/types";
import { typeOptionsStore, artifactStore, traceStore } from "@/hooks";
import { handleCreateLink } from "@/api";
import {
  GenericModal,
  Typography,
  ArtifactInput,
  TypeDirectionInput,
} from "@/components/common";

/**
 * A modal for creating trace links.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "TraceLinkCreatorModal",
  components: { Typography, ArtifactInput, GenericModal, TypeDirectionInput },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      sourceArtifactId: "",
      targetArtifactId: "",
    };
  },
  watch: {
    isOpen(open: boolean) {
      if (!open) return;

      this.sourceArtifactId = "";
      this.targetArtifactId = "";
    },
  },
  computed: {
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
      this.$emit("close");
    },
  },
});
</script>
