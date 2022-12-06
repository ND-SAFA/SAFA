<template>
  <div>
    <v-card
      outlined
      class="my-2 pa-2"
      v-for="(matrix, idx) in model"
      :key="idx"
    >
      <flex-box full-width align="center">
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
          <flex-box justify="center">
            <attribute-chip
              v-for="(detail, idx) in getMatrixDetails(matrix)"
              :key="detail"
              :value="detail"
              :icon="
                idx < 2 ? 'mdi-alpha-a-box-outline' : 'mdi-ray-start-arrow'
              "
            />
          </flex-box>
        </flex-box>
        <generic-icon-button
          icon-id="mdi-close"
          color="error"
          tooltip="Remove trace matrix"
          @click="handleRemoveMatrix(idx)"
        />
      </flex-box>
    </v-card>

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
import { ArtifactLevelSchema } from "@/types";
import { artifactStore, traceStore } from "@/hooks";
import {
  ArtifactTypeInput,
  FlexBox,
  GenericIconButton,
  AttributeChip,
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
    ArtifactTypeInput,
    FlexBox,
    AttributeChip,
  },
  props: {
    value: {
      type: Array as PropType<ArtifactLevelSchema[]>,
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
     * Returns displayable characteristics on a matrix of artifacts.
     * @param matrix - The matrix to get details for.
     */
    getMatrixDetails(matrix: ArtifactLevelSchema): string[] {
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

      return [
        `Source Artifacts: ${sources.length}`,
        `Target Artifacts: ${targets.length}`,
        `Manual Links: ${manual.length}`,
        `Approved Links: ${approved.length}`,
      ];
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
    value(currentValue: ArtifactLevelSchema[]) {
      this.model = currentValue;
    },
    /**
     * Emits changes to the model.
     */
    model(currentValue: ArtifactLevelSchema[]) {
      this.$emit("input", currentValue);
    },
  },
});
</script>
