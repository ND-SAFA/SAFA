<template>
  <div>
    <flex-box
      full-width
      y="4"
      align="center"
      v-for="(matrix, idx) in model"
      :key="idx"
    >
      <flex-box column full-width>
        <flex-box b="2">
          <artifact-type-input
            hide-details
            v-model="matrix.source"
            label="Source Type"
            class="mr-2"
            style="width: 50%"
          />
          <artifact-type-input
            hide-details
            v-model="matrix.target"
            label="Target Type"
            class="mr-2"
            style="width: 50%"
          />
        </flex-box>
        <typography
          secondary
          align="center"
          :value="getMatrixDetails(matrix)"
        />
      </flex-box>
      <generic-icon-button
        icon-id="mdi-close"
        color="error"
        tooltip="Remove trace matrix"
        @click="handleRemoveMatrix(idx)"
      />
    </flex-box>
    <flex-box justify="center">
      <v-btn text color="primary" @click="handleCreateMatrix">
        <v-icon>mdi-plus</v-icon>
        Add New Matrix
      </v-btn>
    </flex-box>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactLevelModel } from "@/types";
import { artifactStore, traceStore } from "@/hooks";
import {
  ArtifactTypeInput,
  FlexBox,
  GenericIconButton,
  Typography,
} from "@/components/common";

/**
 * Creates an array of trace matrices.
 *
 * @emits `input` (ArtifactLevelModel[]) - On matrix change.
 */
export default Vue.extend({
  name: "TraceMatrixCreator",
  components: {
    GenericIconButton,
    Typography,
    ArtifactTypeInput,
    FlexBox,
  },
  props: {
    value: {
      type: Array as PropType<ArtifactLevelModel[]>,
      required: true,
    },
  },
  data() {
    return {
      model: this.value,
    };
  },
  methods: {
    /**
     * Gets the details information on a matrix of artifacts.
     * @param matrix - The matrix to get details for.
     */
    getMatrixDetails(matrix: ArtifactLevelModel): string {
      const sources = artifactStore.getArtifactsByType[matrix.source] || [];
      const targets = artifactStore.getArtifactsByType[matrix.target] || [];
      const manual = traceStore.getTraceLinksByArtifactSets(sources, targets, [
        "manual",
      ]);
      const approved = traceStore.getTraceLinksByArtifactSets(
        sources,
        targets,
        ["approved"]
      );

      return (
        `Source Artifacts: ${sources.length} | Target Artifacts: ${targets.length} | ` +
        `Manual Links: ${manual.length} | Approved Links: ${approved.length}`
      );
    },
    /**
     * Creates a new trace matrix.
     */
    handleCreateMatrix(): void {
      this.model.push({ source: "", target: "" });
    },
    /**
     * Removes a matrix from the list.
     * @param idx - The matrix index to remove.
     */
    handleRemoveMatrix(idx: number) {
      this.model = this.model.filter((_, currentIdx) => currentIdx !== idx);
    },
  },
  watch: {
    /**
     * Updates the model if the value changes.
     */
    value(currentValue: ArtifactLevelModel[]) {
      this.model = currentValue;
    },
    /**
     * Emits changes to the model.
     */
    model(currentValue: ArtifactLevelModel[]) {
      this.$emit("input", currentValue);
    },
  },
});
</script>
