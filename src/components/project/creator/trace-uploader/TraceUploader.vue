<template>
  <v-container>
    <PanelController
      noItemError="No trace links have been uploaded."
      :showError="traceFiles.length === 0"
      :isValidStates="isValidStates"
      @onAdd="isCreateTraceCreatorOpen = true"
      @onIsValid="$emit('onIsValid')"
      @onIsInvalid="$emit('onIsInvalid')"
    >
      <template v-slot:panels>
        <TraceFilePanel
          v-for="(traceFile, i) in traceFiles"
          :key="traceFile.type"
          :traceFile="traceFile"
          :artifactMap="artifactMap"
          @onChange="onChange(i, $event)"
          @onDelete="deleteTraceFile(i)"
          @onIsValid="setFileIsValid(i, true)"
          @onIsInvalid="setFileIsValid(i, false)"
        />
      </template>
    </PanelController>
    <TraceFileCreator
      :isOpen="isCreateTraceCreatorOpen"
      :traceFiles="traceFiles"
      :artifactTypes="artifactTypes"
      @onSubmit="addTraceFile"
      @onClose="isCreateTraceCreatorOpen = false"
    />
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TraceFile } from "@/types/common-components";
import TraceFilePanel from "@/components/project/creator/trace-uploader/TraceFilePanel.vue";
import PanelController from "@/components/project/creator/shared/PanelController.vue";
import TraceFileCreator from "./TraceFileCreator.vue";
import { TraceLink } from "@/types/domain/links";
import { parseTraceFile } from "@/api/parse-api";
import { ParseTraceFileResponse } from "@/types/api";
import { Artifact } from "@/types/domain/artifact";

const DEFAULT_IS_GENERATED = false;
const DEFAULT_VALID_STATE = false;

export default Vue.extend({
  components: {
    TraceFileCreator,
    TraceFilePanel,
    PanelController,
  },
  props: {
    artifactTypes: {
      type: Array as PropType<string[]>,
      required: true,
    },
    artifactMap: {
      type: Object as PropType<Record<string, Artifact>>,
      required: true,
    },
    traceFiles: {
      type: Array as PropType<TraceFile[]>,
      required: true,
    },
  },
  data() {
    return {
      isValidStates: [] as boolean[],
      isCreateTraceCreatorOpen: false,
    };
  },
  computed: {
    isValid(): boolean {
      return this.isValidStates.filter((isValid) => !isValid).length === 0;
    },
  },
  watch: {
    isValid(): void {
      if (this.isValid) {
        this.$emit("onIsValid");
      } else {
        this.$emit("onIsInvalid");
      }
    },
  },
  methods: {
    onChange(i: number, traceFile: TraceFile | undefined): void {
      this.$emit(
        "onChange",
        this.traceFiles.map((a, currentIndex) => {
          if (currentIndex === i) return traceFile;
          return a;
        })
      );
    },
    setFileIsValid(traceFileIndex: number, isValid: boolean): void {
      Vue.set(this.isValidStates, traceFileIndex, isValid);
    },
    deleteTraceFile(i: number): void {
      this.$emit(
        "onChange",
        this.traceFiles.filter((f, index) => index !== i)
      );
    },
    addTraceFile(traceLink: TraceLink): void {
      this.isValidStates = this.isValidStates.concat([DEFAULT_VALID_STATE]);
      this.$emit(
        "onChange",
        this.traceFiles.concat([
          {
            source: traceLink.source,
            target: traceLink.target,
            isGenerated: DEFAULT_IS_GENERATED,
            errors: [],
            traces: [],
          },
        ])
      );
    },
  },
});
</script>
