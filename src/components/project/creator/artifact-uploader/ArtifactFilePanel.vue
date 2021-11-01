<template>
  <FilePanel
    @onChange="onChange"
    @onDelete="$emit('onDelete')"
    :errors="artifactFile.errors"
    :entityNames="artifactNames"
    v-bind:ignoreErrorsFlag.sync="ignoreErrors"
  >
    <template v-slot:title>
      <h3>{{ artifactFile.type }}</h3>
    </template>
  </FilePanel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import FilePanel from "@/components/project/creator/shared/FilePanel.vue";
import type { ArtifactFile } from "@/types/common-components";

import { appModule } from "@/store";
import { parseArtifactFile } from "@/api/parse-api";
import { ParseArtifactFileResponse } from "@/types/api";

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
  data() {
    return {
      ignoreErrors: false,
    };
  },
  computed: {
    isValid(): boolean {
      return this.ignoreErrors || this.artifactFile.file !== undefined;
    },
    artifactNames(): string[] {
      return this.artifactFile.artifacts.map((a) => a.name);
    },
  },
  methods: {
    onChange(file: File | undefined): void {
      if (file === undefined) {
        this.$emit("onChange", {
          ...this.artifactFile,
          file,
          errors: [],
          artifacts: [],
        });
      } else {
        parseArtifactFile(this.artifactFile.type, file).then(
          (res: ParseArtifactFileResponse) => {
            const { artifacts, errors } = res;
            const updatedFile: ArtifactFile = {
              ...this.artifactFile,
              artifacts,
              errors,
              file,
            };
            this.$emit("onChange", updatedFile);
          }
        );
      }
    },
    emitValidationState(): void {
      if (this.isValid) {
        this.$emit("onIsValid");
      } else {
        this.$emit("onIsInvalid");
      }
    },
    underDevelopmentError(): void {
      appModule.onWarning("Viewing parsed artifacts is under development.");
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
