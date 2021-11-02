<template>
  <FilePanel
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
  </FilePanel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import FilePanel from "@/components/project/creator/validation-panels/FilePanel.vue";
import {
  ArtifactMap,
  IGenericFilePanel,
  ValidFileTypes,
} from "@/components/project/creator/uploaders/types";

export default Vue.extend({
  components: {
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
    };
  },
  computed: {
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
});
</script>
