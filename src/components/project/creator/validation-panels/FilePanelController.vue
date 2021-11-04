<template>
  <FilePanel
    :showFileUploader="!isGeneratedToggle"
    @onChange="onChange"
    @onDelete="$emit('onDelete')"
    @onValidate="emitValidationState"
    :errors="errors"
    :entityNames="entityNames"
    v-bind:ignoreErrorsFlag.sync="ignoreErrors"
  >
    <template v-slot:title>
      <h3>{{ title }}</h3>
    </template>

    <template v-slot:before-rows v-if="isTraceFile">
      <GenericSwitch v-model="isGeneratedToggle" label="Generate Trace Links" />
    </template>
  </FilePanel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import FilePanel from "@/components/project/creator/validation-panels/FilePanel.vue";
import {
  ArtifactMap,
  IGenericFilePanel,
  isTraceFile,
  ValidFileTypes,
} from "@/components/project/creator/definitions/types";
import GenericSwitch from "@/components/common/generic/GenericSwitch.vue";

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
    isTraceFile(): boolean {
      return isTraceFile(this.panel.projectFile);
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
    onChange(file: File | undefined): void {
      if (file === undefined) {
        this.$emit("onChange", this.panel.clearFile());
      } else {
        this.panel.parseFile(this.artifactMap, file).then((updatedPanel) => {
          this.$emit("onChange", updatedPanel);
        });
      }
    },
    emitValidationState(isValid: boolean): void {
      if (isValid) {
        this.$emit("onIsValid");
      } else {
        this.$emit("onIsInvalid");
      }
    },
  },
  watch: {
    isGeneratedToggle(isGenerated: boolean) {
      if (isTraceFile(this.panel.projectFile)) {
        this.panel.projectFile.isGenerated = isGenerated;
      }
    },
  },
});
</script>
