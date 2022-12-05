<template>
  <div>
    <file-format-alert />
    <file-input
      v-model="selectedFiles"
      :data-cy="dataCy"
      :errors="errors"
      @clear="handleClear"
    />
    <v-expansion-panels class="mb-4" v-if="selectedFiles.length > 0">
      <v-expansion-panel data-cy="toggle-tim-manage">
        <v-expansion-panel-header>
          Manage Project TIM
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-autocomplete
            filled
            chips
            deletable-chips
            multiple
            v-model="artifactTypes"
            label="Artifact Types"
            :items="typeOptions"
            hint="Select the artifact files. Reads the file name <type>.csv"
            persistent-hint
            data-cy="input-tim-artifacts"
            @change="handleTypesChange"
          />
          <v-autocomplete
            filled
            multiple
            chips
            deletable-chips
            return-object
            v-model="traceMatrices"
            label="Trace Matrices"
            :items="matrixOptions"
            :item-text="(item) => `${item.source} To ${item.target}`"
            hint="Select the trace matrix files. Reads the file name <source>2<target>.csv"
            persistent-hint
            data-cy="input-tim-traces"
            @change="handleTimChange"
          />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactLevelModel, TimModel } from "@/types";
import { FileInput, FileFormatAlert } from "@/components/common";

/**
 * An input for project files.
 *
 * @emits-1 `input` (File[]) - On flat files updated.
 */
export default Vue.extend({
  name: "ProjectFilesInput",
  components: {
    FileFormatAlert,
    FileInput,
  },
  props: {
    dataCy: String,
  },
  data() {
    return {
      selectedFiles: [] as File[],
      tim: undefined as TimModel | undefined,
      artifactTypes: [] as string[],
      traceMatrices: [] as ArtifactLevelModel[],
    };
  },
  computed: {
    /**
     * @return Generated artifact types based on file names.
     */
    typeOptions(): string[] {
      return this.selectedFiles
        .map(({ name }) => name.split(".")[0])
        .filter((name) => name !== "tim");
    },
    /**
     * @return Generated trace matrices based on file names.
     */
    matrixOptions(): ArtifactLevelModel[] {
      return this.artifactTypes
        .map((source) =>
          this.artifactTypes.map((target) => ({ source, target }))
        )
        .reduce((acc, cur) => [...acc, ...cur], []);
    },
    /**
     * @return Any errors on uploaded files.
     */
    errors(): string[] {
      return this.selectedFiles.length === 0 ||
        this.selectedFiles.find(({ name }) => name === "tim.json")
        ? []
        : ["Missing project TIM. Please create one below."];
    },
  },
  methods: {
    /**
     * Clears the current tim file data.
     */
    handleClear(): void {
      this.tim = undefined;
      this.artifactTypes = [];
      this.traceMatrices = [];
    },
    /**
     * Selects relevant trace matrices when the types change, and updates the tim file.
     */
    handleTypesChange(): void {
      this.traceMatrices = this.matrixOptions.filter(({ source, target }) =>
        this.selectedFiles.find(
          ({ name }) => name === `${source}2${target}.csv`
        )
      );

      this.handleTimChange();
    },
    /**
     * Creates a new tim file when the inputs change.
     */
    handleTimChange(): void {
      this.tim = {
        DataFiles: this.artifactTypes
          .map((type) => ({ [type]: { File: `${type}.csv` } }))
          .reduce((acc, cur) => ({ ...acc, ...cur }), {}),
        ...this.traceMatrices
          .map(({ source, target }) => ({
            [`${source}2${target}`]: {
              Source: source,
              Target: target,
              File: `${source}2${target}.csv`,
            },
          }))
          .reduce((acc, cur) => ({ ...acc, ...cur }), {}),
      } as TimModel;

      this.selectedFiles = [
        ...this.selectedFiles.filter(({ name }) => name !== "tim.json"),
        new File([JSON.stringify(this.tim)], "tim.json", {
          type: "application/json",
        }),
      ];
    },
  },
  watch: {
    /**
     * Emits changes to selected files.
     * If a tim file is loaded, it is parsed so that it can be edited.
     */
    selectedFiles(files: File[]) {
      this.$emit("input", files);

      const timFile = files.find(({ name }) => name === "tim.json");

      if (!timFile) return;

      const reader = new FileReader();

      reader.addEventListener("load", (event) => {
        this.tim = JSON.parse(String(event.target?.result));

        this.artifactTypes = Object.keys(this.tim?.DataFiles || {});
        this.traceMatrices = Object.values(this.tim || {})
          .filter(({ Source, Target }) => Source && Target)
          .map(({ Source, Target }) => ({
            source: String(Source),
            target: String(Target),
          }));
      });

      reader.readAsText(timFile);
    },
  },
});
</script>
