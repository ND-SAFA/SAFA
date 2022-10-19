<template>
  <file-panel
    :show-file-uploader="!isGeneratedToggle"
    @change="handleChange"
    @delete="$emit('delete')"
    @validate="setValidationState"
    :errors="errors"
    :entity-names="entityNames"
    :entities-are-fab="!isTracePanel"
    :is-loading="isLoading"
    v-bind:ignore-errors-flag.sync="ignoreErrors"
  >
    <template v-slot:title>
      <typography el="h2" variant="subtitle" :value="title" />
    </template>

    <template v-slot:before-rows v-if="isTracePanel">
      <generic-switch
        v-model="isGeneratedToggle"
        label="Generate Trace Links"
      />
      <gen-method-input v-if="isGeneratedToggle" v-model="method" />
    </template>
  </file-panel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import {
  ArtifactMap,
  IGenericFilePanel,
  ModelType,
  ValidFileTypes,
} from "@/types";
import { isTracePanel } from "@/util";
import { GenericSwitch, GenMethodInput, Typography } from "@/components/common";
import FilePanel from "./FilePanel.vue";

/**
 * Controls a file panel.
 *
 * @emits-1 `delete` - On delete.
 * @emits-2 `validate` (isValid: boolean) - On validate.
 */
export default Vue.extend({
  name: "FilePanelController",
  components: {
    GenMethodInput,
    GenericSwitch,
    FilePanel,
    Typography,
  },
  props: {
    artifactMap: {
      type: Object as PropType<ArtifactMap>,
      required: true,
    },
    panel: {
      type: Object as PropType<IGenericFilePanel<ArtifactMap, ValidFileTypes>>,
      required: true,
    },
  },
  data() {
    return {
      isLoading: false,
      ignoreErrors: false,
      isGeneratedToggle: false,
    };
  },
  computed: {
    /**
     * @return Whether this is a trace panel.
     */
    isTracePanel(): boolean {
      return isTracePanel(this.panel);
    },
    /**
     * @return Whether this panel is valid.
     */
    isValid(): boolean {
      return this.panel.getIsValid();
    },
    /**
     * @return Any errors in this panel.
     */
    errors(): string[] {
      return this.panel.projectFile.errors;
    },
    /**
     * @return The title of the panel.
     */
    title(): string {
      return this.panel.title;
    },
    /**
     * @return The names of the entities in the panel.
     */
    entityNames(): string[] {
      return this.panel.entityNames;
    },
    method: {
      get(): ModelType {
        if (isTracePanel(this.panel)) {
          return this.panel.projectFile.method;
        } else {
          return ModelType.NLBert;
        }
      },
      set(newMethod: ModelType): void {
        if (isTracePanel(this.panel)) {
          this.panel.projectFile.method = newMethod;
        }
      },
    },
  },
  methods: {
    /**
     * Parses added files.
     * @param file - The file to parse.
     */
    async handleChange(file: File | undefined): Promise<void> {
      if (file === undefined) {
        this.panel.clearPanel();
      } else {
        this.isLoading = true;
        await this.panel.parseFile(this.artifactMap, file);
        this.isLoading = false;
      }
    },
    /**
     * Sets whether the panel is valid, and emits that change.
     * @param isValid - Whether the panel is valid.
     */
    setValidationState(isValid: boolean): void {
      this.panel.projectFile.isValid = isValid;
      this.$emit("validate", isValid);
    },
  },
  watch: {
    /**
     * Generates trace files when generate is toggled on.
     */
    isGeneratedToggle(isGenerated: boolean) {
      if (!isTracePanel(this.panel)) return;

      this.panel.projectFile.isGenerated = isGenerated;
      this.panel.clearPanel();
    },
  },
});
</script>
