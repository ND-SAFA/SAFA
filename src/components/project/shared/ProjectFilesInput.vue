<template>
  <div>
    <generic-file-selector v-model="selectedFiles" :data-cy="dataCy" />
    <v-expansion-panels class="mb-2 elevation-0">
      <v-expansion-panel>
        <v-expansion-panel-header>
          Manage Uploaded Files
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-combobox
            filled
            chips
            deletable-chips
            multiple
            v-model="artifactTypes"
            label="Artifact Types"
            @change="handleTimChange"
            hint="Enter the prefixes of artifact files."
            persistent-hint
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
            :item-text="(item) => `${item.source} -> ${item.target}`"
            hint="Select the trace matrices files."
            persistent-hint
            @change="handleTimChange"
          />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
    <file-format-alert />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactLevelModel } from "@/types";
import { GenericFileSelector, FileFormatAlert } from "@/components/common";

type TimModel = {
  DataFiles: {
    [artifactType: string]: {
      File: string;
    };
  };
} & {
  [traceType: string]: {
    Source: string;
    Target: string;
  };
};

/**
 * An input for project files.
 *
 * @emits-1 `input` (File[]) - On flat files updated.
 */
export default Vue.extend({
  name: "ProjectFilesInput",
  components: {
    FileFormatAlert,
    GenericFileSelector,
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
    matrixOptions(): ArtifactLevelModel[] {
      return this.artifactTypes
        .map((source) =>
          this.artifactTypes.map((target) => ({ source, target }))
        )
        .reduce((acc, cur) => [...acc, ...cur], []);
    },
  },
  methods: {
    handleTimChange() {
      this.tim = {
        DataFiles: this.artifactTypes
          .map((type) => ({ [type]: { File: `${type}.csv` } }))
          .reduce((acc, cur) => ({ ...acc, ...cur }), {}),
        ...this.traceMatrices
          .map(({ source, target }) => ({
            [`${source}2${target}`]: { Source: source, Target: target },
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
