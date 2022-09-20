<template>
  <generic-modal
    title="Generate Trace Links"
    :is-open="isOpen"
    @close="handleClose"
    size="l"
    data-cy="modal-trace-generate"
  >
    <template v-slot:body>
      <typography
        el="p"
        y="2"
        value="Select which sets of artifact types that you would like to generate links between."
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
          <flex-box>
            <generic-switch
              :value="isCustomModel(idx)"
              label="Use Custom Model"
              @input="toggleCustomModel(idx)"
            />
            <gen-method-input
              v-if="!isCustomModel(idx)"
              v-model="matrix.method"
            />
            <custom-model-input v-else />
          </flex-box>
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
        Generate
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue from "vue";
import { GeneratedMatrixModel, ModelType, TypeMatrixModel } from "@/types";
import { appStore } from "@/hooks";
import { handleGenerateLinks } from "@/api";
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
        this.isValid = matrices
          .map((matrix) => !!matrix.source && !!matrix.target)
          .reduce((acc, cur) => acc && cur, true);
      },
    },
  },
  computed: {
    /**
     * @return Whether this modal is open.
     */
    isOpen(): boolean {
      return appStore.isTraceLinkGeneratorOpen;
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
      handleGenerateLinks(this.matrices, {});
      this.handleClose();
    },
    /**
     * Closes the modal.
     */
    handleClose(): void {
      appStore.toggleTraceLinkGenerator();
    },
  },
});
</script>
