<template>
  <generic-modal
    :title="modalTitle"
    :is-open="isOpen"
    @close="handleClose"
    size="l"
    data-cy="modal-trace-generate"
  >
    <template v-slot:body>
      <typography el="p" y="2" :value="modalDescription" />

      <custom-model-input v-if="isTraining" v-model="model" />

      <flex-box
        full-width
        y="4"
        align="center"
        v-for="(matrix, idx) in matrices"
        :key="idx"
      >
        <flex-box column full-width>
          <flex-box b="2">
            <artifact-type-input
              hide-details
              v-model="matrix.source"
              label="Source Type"
              class="mr-2"
            />
            <artifact-type-input
              hide-details
              v-model="matrix.target"
              label="Target Type"
              class="mr-2"
            />
          </flex-box>
          <flex-box v-if="!isTraining">
            <generic-switch
              :value="isCustomModel(idx)"
              label="Use Custom Model"
              @input="toggleCustomModel(idx)"
            />
            <gen-method-input
              v-if="!isCustomModel(idx)"
              v-model="matrix.method"
            />
            <custom-model-input v-else v-model="matrix.model" />
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
    </template>

    <template v-slot:actions>
      <v-spacer />
      <v-btn
        :disabled="!isValid"
        :loading="isLoading"
        color="primary"
        data-cy="button-trace-generate"
        @click="handleSubmit"
      >
        {{ saveButtonLabel }}
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue from "vue";
import {
  GeneratedMatrixModel,
  GeneratorOpenState,
  ModelType,
  TrainedModel,
  TypeMatrixModel,
} from "@/types";
import { appStore, artifactStore, traceStore } from "@/hooks";
import { handleGenerateLinks, handleTrainModel } from "@/api";
import {
  ArtifactTypeInput,
  FlexBox,
  GenericIconButton,
  GenericModal,
  Typography,
  GenMethodInput,
  CustomModelInput,
  GenericSwitch,
} from "@/components/common";

/**
 * A modal for generating trace links.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "TraceLinkGeneratorModal",
  components: {
    GenericSwitch,
    CustomModelInput,
    GenMethodInput,
    GenericIconButton,
    Typography,
    ArtifactTypeInput,
    FlexBox,
    GenericModal,
  },
  data() {
    return {
      isLoading: false,
      isValid: false,
      customModels: [] as number[],
      model: undefined as TrainedModel | undefined,
      matrices: [
        { source: "", target: "", method: ModelType.NLBert },
      ] as GeneratedMatrixModel[],
    };
  },
  watch: {
    isOpen(open: boolean) {
      if (!open) return;

      this.isLoading = false;
      this.isValid = false;
      this.matrices = [{ source: "", target: "", method: ModelType.NLBert }];
    },
    /**
     * Validates that all matrices are valid on change.
     */
    matrices: {
      deep: true,
      handler(matrices: TypeMatrixModel[]) {
        if (this.isTraining) {
          this.isValid =
            !!this.model &&
            matrices
              .map((matrix) => !!matrix.source && !!matrix.target)
              .reduce((acc, cur) => acc && cur, true);
        } else {
          this.isValid = matrices
            .map((matrix) => !!matrix.source && !!matrix.target)
            .reduce((acc, cur) => acc && cur, true);
        }
      },
    },
  },
  computed: {
    /**
     * @return Whether this modal is open.
     */
    isOpen(): GeneratorOpenState {
      return appStore.isTraceLinkGeneratorOpen;
    },
    /**
     * @return Whether this modal is set to train models
     */
    isTraining(): boolean {
      return this.isOpen === "train";
    },
    /**
     * @return The title of this modal.
     */
    modalTitle(): string {
      return this.isTraining ? "Train Models" : "Generate Trace Links";
    },
    /**
     * @return The save button label.
     */
    saveButtonLabel(): string {
      return this.isTraining ? "Train" : "Generate";
    },
    /**
     * @return The description of this modal.
     */
    modalDescription(): string {
      return this.isTraining
        ? "Select which sets of artifact types that you would like to train your model on. " +
            "Make sure that all links between these artifacts are complete, as both existing and non-existing links " +
            "will inform the model."
        : "Select which sets of artifact types that you would like to generate links between.";
    },
  },
  methods: {
    /**
     * Returns whether the model is custom.
     * @param modelIdx - The model index to check.
     * @return Whether it uses a custom model.
     */
    isCustomModel(modelIdx: number): boolean {
      return this.customModels.includes(modelIdx);
    },
    /**
     * Toggles whether a model is set to custom.
     * @param modelIdx - The model index to toggle.
     */
    toggleCustomModel(modelIdx: number): void {
      if (this.isCustomModel(modelIdx)) {
        this.customModels = this.customModels.filter((idx) => idx !== modelIdx);
      } else {
        this.customModels.push(modelIdx);
      }

      this.matrices[modelIdx].model = undefined;
      this.matrices[modelIdx].method = ModelType.NLBert;
    },
    getMatrixDetails(matrix: GeneratedMatrixModel): string {
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
      this.matrices.push({ source: "", target: "", method: ModelType.NLBert });
    },
    /**
     * Removes a matrix from the list.
     * @param idx - The matrix index to remove.
     */
    handleRemoveMatrix(idx: number) {
      this.matrices = this.matrices.filter(
        (_, currentIdx) => currentIdx !== idx
      );
    },
    /**
     * Attempts to generate the selected trace links.
     */
    handleSubmit(): void {
      if (this.isTraining) {
        if (!this.model) return;

        handleTrainModel(this.model, this.matrices, {});
      } else {
        handleGenerateLinks(this.matrices, {});
      }

      this.handleClose();
    },
    /**
     * Closes the modal.
     */
    handleClose(): void {
      appStore.closeTraceLinkGenerator();
    },
  },
});
</script>
