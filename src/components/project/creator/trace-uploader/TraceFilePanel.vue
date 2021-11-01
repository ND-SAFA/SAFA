<template>
  <FilePanel
    @onChange="onChange"
    @onDelete="$emit('onDelete')"
    :showFileUploader="!traceFile.isGenerated"
    :errors="errors"
    :entityNames="traceIds"
    v-bind:ignoreErrorsFlag.sync="ignoreErrors"
  >
    <template v-slot:title>
      <label>
        {{ traceFile.source }}
      </label>
      <v-icon>mdi-arrow-right</v-icon>
      <label>
        {{ traceFile.target }}
      </label>
    </template>

    <template v-slot:before-rows>
      <v-row>
        <v-col cols="9" align-self="center"> Generate Links: </v-col>
        <v-col cols="3" align-self="center">
          <v-switch v-model="traceFile.isGenerated" />
        </v-col>
      </v-row>
    </template>
  </FilePanel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TraceFile } from "@/types/common-components";
import FilePanel from "@/components/project/creator/shared/FilePanel.vue";
import { Artifact } from "@/types/domain/artifact";
import { TraceLink } from "@/types/domain/links";
import { ParseTraceFileResponse } from "@/types/api";
import { parseTraceFile } from "@/api/parse-api";

export default Vue.extend({
  components: {
    FilePanel,
  },
  props: {
    artifactMap: {
      type: Object as PropType<Record<string, Artifact>>,
      required: true,
    },
    traceFile: {
      type: Object as PropType<TraceFile>,
      required: true,
    },
  },
  data() {
    return {
      localErrors: [] as string[],
      ignoreErrors: false,
    };
  },
  computed: {
    isValid(): boolean {
      return (
        this.ignoreErrors ||
        this.traceFile.file !== undefined ||
        this.traceFile.isGenerated
      );
    },
    errors(): string[] {
      return (
        this.traceFile.errors === undefined ? [] : this.traceFile.errors
      ).concat(this.localErrors);
    },
    traces(): TraceLink[] {
      return this.traceFile.traces;
    },
    traceIds(): string[] {
      return this.traceFile.traces
        .filter((t) => this.getTraceError(t) === undefined)
        .map((t) => `${t.source}-${t.target}`);
    },
  },
  methods: {
    onChange(file: File | undefined): void {
      if (file === undefined) {
        this.$emit("onChange", {
          ...this.traceFile,
          file,
          traces: [],
          errors: [],
        });
      } else {
        // eslint-disable-next-line no-undef
        parseTraceFile(file).then((res: ParseTraceFileResponse) => {
          const { traces, errors } = res;
          const updatedTraceFile: TraceFile = {
            ...this.traceFile,
            traces,
            errors,
            file,
          };
          this.$emit("onChange", updatedTraceFile);
        });
      }
    },
    emitValidationState(): void {
      if (this.isValid) {
        this.$emit("onIsValid");
      } else {
        this.$emit("onIsInvalid");
      }
    },
    getTraceError(traceLink: TraceLink): string | undefined {
      const { source, target } = traceLink;
      if (!(source in this.artifactMap)) {
        return `Artifact ${source} in does not exist.`;
      } else if (!(target in this.artifactMap)) {
        return `Artifact ${target} does not exist.`;
      } else {
        const sourceArtifact = this.artifactMap[source];
        const targetArtifact = this.artifactMap[target];

        if (sourceArtifact.type !== this.traceFile.source) {
          return `${sourceArtifact.name} is not of type ${this.traceFile.source}.`;
        }

        if (targetArtifact.type !== this.traceFile.target) {
          return `${targetArtifact.name} is not of type ${this.traceFile.target}.`;
        }
      }
    },
  },
  watch: {
    isValid(): void {
      this.emitValidationState();
    },
    traces(traces: TraceLink[]) {
      traces.forEach((traceLink) => {
        const error = this.getTraceError(traceLink);
        if (error !== undefined) {
          this.localErrors = this.localErrors.concat([error]);
        }
      });
    },
  },
  mounted() {
    this.emitValidationState();
  },
});
</script>
