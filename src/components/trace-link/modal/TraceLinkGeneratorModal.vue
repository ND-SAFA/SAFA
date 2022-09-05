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
        y="2"
        align="center"
        v-for="(matrix, idx) in matrices"
        :key="idx"
      >
        <v-select
          filled
          hide-details
          label="Model"
          v-model="matrix.method"
          :items="modelOptions"
          class="mr-2"
          item-value="id"
          item-text="name"
        />
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
import {
  GeneratedMatrixModel,
  ModelType,
  SelectOption,
  TypeMatrixModel,
} from "@/types";
import { traceModelOptions } from "@/util";
import { appStore } from "@/hooks";
import { handleGenerateLinks } from "@/api";
import {
  ArtifactTypeInput,
  FlexBox,
  GenericIconButton,
  GenericModal,
  Typography,
} from "@/components/common";

/**
 * A modal for generating trace links.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "TraceLinkGeneratorModal",
  components: {
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
      matrices: [
        { source: "", target: "", method: ModelType.TBERT },
      ] as GeneratedMatrixModel[],
    };
  },
  watch: {
    isOpen(open: boolean) {
      if (!open) return;

      this.isLoading = false;
      this.isValid = false;
      this.matrices = [{ source: "", target: "", method: ModelType.TBERT }];
    },
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
    /**
     * @return The trace generation model types.
     */
    modelOptions(): SelectOption[] {
      return traceModelOptions();
    },
  },
  methods: {
    /**
     * Creates a new trace matrix.
     */
    handleCreateMatrix(): void {
      this.matrices.push({ source: "", target: "", method: ModelType.TBERT });
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
      this.isLoading = true;
      handleGenerateLinks(this.matrices, {
        onSuccess: () => {
          this.isLoading = false;
          this.handleClose();
        },
        onError: () => (this.isLoading = false),
      });
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
