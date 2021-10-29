<template>
  <FilePanel @onChange="onChange" @onDelete="$emit('onDelete')">
    <template v-slot:title>
      <h3>{{ artifactFile.type }}</h3>
    </template>
  </FilePanel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactFile } from "@/types/common-components";
import FilePanel from "@/components/project/creator/shared/FilePanel.vue";

export default Vue.extend({
  components: {
    FilePanel,
  },
  props: {
    artifactFile: {
      type: Object as PropType<ArtifactFile>,
      required: true,
    },
  },
  computed: {
    isValid(): boolean {
      return this.artifactFile.file !== undefined;
    },
  },
  methods: {
    onChange(file: File): void {
      this.$emit("onChange", { ...this.artifactFile, file });
    },

    emitValidationState(): void {
      if (this.isValid) {
        this.$emit("onIsValid");
      } else {
        this.$emit("onIsInvalid");
      }
    },
  },
  watch: {
    isValid(): void {
      this.emitValidationState();
    },
  },
  mounted() {
    this.emitValidationState();
  },
});
</script>
