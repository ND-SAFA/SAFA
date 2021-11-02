<template>
  <v-container>
    <ValidatedPanels
      :noItemError="noItemError"
      :showError="projectFiles.length === 0"
      :isValidStates="isValidStates"
      @onAdd="isCreatorOpen = true"
      @onIsValid="$emit('onIsValid')"
      @onIsInvalid="$emit('onIsInvalid')"
    >
      <template v-slot:panels>
        <GenericFilePanel
          v-for="(panel, i) in panels"
          :key="panel.title"
          :panel="panel"
          :artifactMap="artifactMap"
          @onChange="onChange(i, $event)"
          @onDelete="deleteFile(i)"
          @onIsValid="setFileIsValid(i, true)"
          @onIsInvalid="setFileIsValid(i, false)"
        />
      </template>
    </ValidatedPanels>

    <slot
      name="creator"
      v-bind:isCreatorOpen="isCreatorOpen"
      v-bind:onAddFile="addFile"
      v-bind:onClose="onCloseCreator"
    />
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import ValidatedPanels from "@/components/project/creator/validation-panels/ValidatedPanels.vue";
import {
  ArtifactMap,
  IGenericFilePanel,
  IGenericUploader,
  ValidFileTypes,
} from "@/components/project/creator/uploaders/types";
import { ProjectFile } from "@/types/common-components";
import { TraceLink } from "@/types/domain/links";
import GenericFilePanel from "@/components/project/creator/validation-panels/FilePanelController.vue";

const DEFAULT_VALID_STATE = false;
type ValidPayloads = string | TraceLink;

export default Vue.extend({
  components: {
    ValidatedPanels,
    GenericFilePanel,
  },
  props: {
    artifactMap: {
      type: Object as PropType<ArtifactMap>,
      required: true,
    },
    uploader: {
      type: Object as PropType<
        IGenericUploader<ArtifactMap, ValidPayloads, ValidFileTypes>
      >,
      required: true,
    },
    noItemError: {
      type: String,
      default: "No entities have been created.",
    },
  },
  data() {
    return {
      isValidStates: [] as boolean[],
      isCreatorOpen: false,
    };
  },

  computed: {
    panels(): IGenericFilePanel<ArtifactMap, ValidFileTypes>[] {
      return this.uploader.panels;
    },
    isValid(): boolean {
      return this.isValidStates.filter((isValid) => !isValid).length === 0;
    },
    projectFiles(): ProjectFile[] {
      return this.uploader.panels.map((p) => p.projectFile);
    },
  },
  methods: {
    onCloseCreator(): void {
      this.isCreatorOpen = false;
    },
    onChange(
      i: number,
      panel: IGenericFilePanel<ArtifactMap, ValidFileTypes>
    ): void {
      this.$emit(
        "onChange",
        this.panels.map((a, currentIndex) => {
          if (currentIndex === i) return panel;
          return a;
        })
      );
    },
    setFileIsValid(artifactFileIndex: number, isValid: boolean): void {
      Vue.set(this.isValidStates, artifactFileIndex, isValid);
    },
    deleteFile(i: number): void {
      console.log("DELETING FILE");
      this.$emit(
        "onChange",
        this.panels.filter((f, index) => index !== i)
      );
    },
    addFile(payload: string | TraceLink): void {
      this.isValidStates = this.isValidStates.concat([DEFAULT_VALID_STATE]);
      const newPanel = this.uploader.createNewPanel(payload);
      this.$emit("onChange", this.panels.concat([newPanel]));
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
});
</script>
