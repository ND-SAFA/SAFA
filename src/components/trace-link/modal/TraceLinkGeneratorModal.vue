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

      <flex-box>
        <generic-switch
          v-if="!isTraining"
          :value="isCustomModel"
          label="Use Custom Model"
          @input="toggleCustomModel"
        />
        <gen-method-input
          v-if="!isCustomModel && !isTraining"
          v-model="method"
        />
        <custom-model-input v-else v-model="model" />
      </flex-box>

      <typography
        v-if="!isCustomModel"
        error
        value="Predefined models will not produce the best results. Please use a custom model to generate higher quality links."
      />

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
  ArtifactLevelModel,
  GeneratorOpenState,
  ModelType,
  TrainedModel,
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
      isCustomModel: true,
      method: undefined as ModelType | undefined,
      model: undefined as TrainedModel | undefined,
      matrices: [{ source: "", target: "" }] as ArtifactLevelModel[],
    };
  },
  watch: {
    isOpen(open: boolean) {
      if (!open) return;

      this.isLoading = false;
      this.isValid = false;
      this.isCustomModel = true;
      this.method = undefined;
      this.model = undefined;
      this.matrices = [{ source: "", target: "" }];
    },
    /**
     * Validates that all matrices are valid on change.
     */
    matrices: {
      deep: true,
      handler() {
        this.isValid = this.isEverythingValid;
      },
    },
    model() {
      this.isValid = this.isEverythingValid;
    },
    method() {
      this.isValid = this.isEverythingValid;
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
    /**
     * @return Whether the current matrices are valid.
     */
    areMatricesValid(): boolean {
      return this.matrices
        .map((matrix) => !!matrix.source && !!matrix.target)
        .reduce((acc, cur) => acc && cur, true);
    },
    /**
     * @return Whether the current request is valid.
     */
    isEverythingValid(): boolean {
      if (this.isTraining) {
        return !!this.model && this.areMatricesValid;
      } else {
        return (!!this.model || !!this.method) && this.areMatricesValid;
      }
    },
  },
  methods: {
    /**
     * Toggles whether a model is set to custom.
     */
    toggleCustomModel(): void {
      this.isCustomModel = !this.isCustomModel;
      this.model = undefined;
      this.method = undefined;
    },
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
      this.matrices.push({ source: "", target: "" });
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
      if (this.isTraining && this.model) {
        this.isLoading = true;
        handleTrainModel(this.model, this.matrices, {
          onComplete: () => (this.isLoading = false),
        });
      } else {
        this.isLoading = true;
        handleGenerateLinks(this.method, this.model, this.matrices, {
          onComplete: () => (this.isLoading = false),
        });
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
