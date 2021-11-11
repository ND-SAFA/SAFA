<template>
  <FilePanel
    :showFileUploader="!isGeneratedToggle"
    @onChange="onChange"
    @onDelete="$emit('onDelete')"
    @onValidate="setValidationState"
    :errors="errors"
    :entityNames="entityNames"
    :entities-are-fab="!isTracePanel"
    v-bind:ignoreErrorsFlag.sync="ignoreErrors"
  >
    <template v-slot:title>
      <h3>{{ title }}</h3>
    </template>

    <template v-slot:before-rows v-if="isTracePanel">
      <GenericSwitch v-model="isGeneratedToggle" label="Generate Trace Links" />
    </template>
  </FilePanel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactMap, IGenericFilePanel, ValidFileTypes } from "@/types";
import { isTracePanel } from "@/util";
import { GenericSwitch, FilePanel } from "@/components";

export default Vue.extend({
  components: {
    GenericSwitch,
    FilePanel,
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
      ignoreErrors: false,
      isGeneratedToggle: false,
    };
  },
  computed: {
    isTracePanel(): boolean {
      return isTracePanel(this.panel);
    },
    isValid(): boolean {
      return this.panel.getIsValid();
    },
    errors(): string[] {
      return this.panel.projectFile.errors;
    },
    title(): string {
      return this.panel.title;
    },
    entityNames(): string[] {
      return this.panel.entityNames;
    },
  },
  methods: {
    async onChange(file: File | undefined): Promise<void> {
      if (file === undefined) {
        this.panel.clearPanel();
      } else {
        await this.panel.parseFile(this.artifactMap, file);
      }
    },
    setValidationState(isValid: boolean): void {
      this.panel.projectFile.isValid = isValid;
    },
  },
  watch: {
    async isGeneratedToggle(isGenerated: boolean) {
      if (isTracePanel(this.panel)) {
        this.panel.projectFile.isGenerated = isGenerated;
        if (isGenerated) {
          await this.panel.generateTraceLinks(this.artifactMap);
        } else {
          this.panel.clearPanel();
        }
      }
    },
  },
});
</script>
