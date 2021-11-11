<template>
  <v-container>
    <ValidatedPanels
      :itemName="itemName"
      :showError="projectFiles.length === 0"
      :isValidStates="isValidStates"
      :isButtonDisabled="isCreatorOpen"
      :defaultValidState="defaultValidState"
      @onAdd="isCreatorOpen = true"
      @onIsValid="$emit('onIsValid')"
      @onIsInvalid="$emit('onIsInvalid')"
    >
      <template v-slot:panels>
        <FilePanelController
          v-for="(panel, i) in panels"
          :key="panel.title"
          :panel="panel"
          :artifactMap="artifactMap"
          @onChange="onChange(i, $event)"
          @onDelete="deleteFile(i)"
        />
        <slot
          name="creator"
          v-bind:isCreatorOpen="isCreatorOpen"
          v-bind:onAddFile="addFile"
          v-bind:onClose="onCloseCreator"
        />
      </template>
    </ValidatedPanels>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import {
  ArtifactMap,
  IGenericFilePanel,
  IGenericUploader,
  ValidFileTypes,
  ProjectFile,
  TraceLink,
  ValidPayloads,
} from "@/types";
import FilePanelController from "./FilePanelController.vue";
import ValidatedPanels from "./ValidatedPanels.vue";

export default Vue.extend({
  components: {
    ValidatedPanels,
    FilePanelController,
  },
  props: {
    itemName: {
      type: String,
      required: true,
    },
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
    defaultValidState: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      isCreatorOpen: false,
    };
  },

  computed: {
    isValidStates(): boolean[] {
      return this.panels.map((p) => p.projectFile.isValid);
    },
    panels(): IGenericFilePanel<ArtifactMap, ValidFileTypes>[] {
      return this.uploader.panels;
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
    deleteFile(i: number): void {
      this.$emit(
        "onChange",
        this.panels.filter((f, index) => index !== i)
      );
      if (this.panels.length === 0) {
        this.$emit("onIsInvalid");
      }
    },
    addFile(payload: string | TraceLink): void {
      const newPanel = this.uploader.createNewPanel(payload);
      this.$emit("onChange", this.panels.concat([newPanel]));
    },
  },
});
</script>
