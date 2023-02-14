<template>
  <div>
    <typography el="h2" variant="subtitle" value="Generate Trace Links" />
    <typography el="p" b="4" :value="modalDescription" />
    <custom-model-input v-model="model" />
    <trace-matrix-creator v-model="matrices" />
    <v-btn
      block
      :disabled="!isValid"
      :loading="isLoading"
      color="primary"
      data-cy="button-trace-generate"
      class="mt-2"
      @click="handleSubmit"
    >
      Generate Trace Links
    </v-btn>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { ArtifactLevelSchema, ModelType, GenerationModelSchema } from "@/types";
import { handleGenerateLinks } from "@/api";
import { Typography, CustomModelInput } from "@/components/common";
import { TraceMatrixCreator } from "../save";

/**
 * Displays inputs for generating trace links.
 *
 * @emits `submit` - On submit.
 */
export default defineComponent({
  name: "TraceLinkGenerator",
  components: {
    TraceMatrixCreator,
    CustomModelInput,
    Typography,
  },
  props: {
    isOpen: Boolean,
  },
  data() {
    return {
      isLoading: false,
      isValid: false,
      method: undefined as ModelType | undefined,
      model: undefined as GenerationModelSchema | undefined,
      matrices: [{ source: "", target: "" }] as ArtifactLevelSchema[],
    };
  },
  computed: {
    /**
     * @return The description of this modal.
     */
    modalDescription(): string {
      return "Select which sets of artifact types that you would like to generate links between.";
    },
    /**
     * @return Whether the current matrices are valid.
     */
    areMatricesValid(): boolean {
      return this.matrices
        .map(
          (matrix: ArtifactLevelSchema) => !!matrix.source && !!matrix.target
        )
        .reduce((acc: boolean, cur: boolean) => acc && cur, true);
    },
    /**
     * @return Whether the current request is valid.
     */
    isEverythingValid(): boolean {
      return !!this.model && this.areMatricesValid;
    },
  },
  watch: {
    /**
     * Reset the state when opened.
     */
    isOpen(open: boolean) {
      if (!open) return;

      this.reset();
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
  },
  methods: {
    /**
     * Resets this component's data.
     */
    reset(): void {
      this.isLoading = false;
      this.isValid = false;
      this.method = undefined;
      this.model = undefined;
      this.matrices = [{ source: "", target: "" }];
    },
    /**
     * Attempts to generate the selected trace links.
     */
    handleSubmit(): void {
      if (!this.model) return;

      this.isLoading = true;
      handleGenerateLinks(undefined, this.model, this.matrices, {
        onComplete: () => {
          this.reset();
          this.$emit("submit");
        },
      });
    },
  },
});
</script>
