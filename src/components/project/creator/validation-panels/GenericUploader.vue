<template>
  <v-container>
    <validated-panels
      :itemName="itemName"
      :showError="projectFiles.length === 0"
      :isValidStates="isValidStates"
      :isButtonDisabled="isCreatorOpen"
      :defaultValidState="defaultValidState"
      @add="isCreatorOpen = true"
      @upload:valid="$emit('upload:valid')"
      @upload:invalid="$emit('upload:invalid')"
    >
      <template v-slot:panels>
        <v-expansion-panels multiple v-model="openPanelIndexes">
          <file-panel-controller
            v-for="(panel, i) in panels"
            :key="panel.title"
            :panel="panel"
            :artifactMap="artifactMap"
            @change="handleChange(i, $event)"
            @delete="handleDeleteFile(i)"
            @validate="handleValidateChange(i, $event)"
          />
        </v-expansion-panels>
        <slot
          name="creator"
          v-bind:isCreatorOpen="isCreatorOpen"
          v-bind:onAddFile="handleAddFile"
          v-bind:onClose="handleCloseCreator"
        />
      </template>
    </validated-panels>
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
  ValidPayloads,
  Link,
} from "@/types";
import FilePanelController from "./FilePanelController.vue";
import ValidatedPanels from "./ValidatedPanels.vue";

/**
 * A generic file uploader.
 *
 * @emits-1 `upload:valid` - On upload is valid.
 * @emits-2 `upload:invalid` - On upload is invalid.
 * @emits-3 `change` - On change.
 */
export default Vue.extend({
  name: "GenericUploader",
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
  data: () => ({
    isCreatorOpen: false,
    openPanelIndexes: [] as number[],
  }),
  computed: {
    /**
     * @return Whether all panels are valid.
     */
    isValidStates(): boolean[] {
      return this.panels.map((p) => p.projectFile.isValid);
    },
    /**
     * @return All panels.
     */
    panels() {
      return this.uploader.panels;
    },
    /**
     * @return All project files.
     */
    projectFiles(): ProjectFile[] {
      return this.uploader.panels.map((p) => p.projectFile);
    },
  },
  methods: {
    /**
     * Closes the creator.
     */
    handleCloseCreator(): void {
      this.isCreatorOpen = false;
    },
    /**
     * Emits changed panels.
     */
    handleChange(
      i: number,
      panel: IGenericFilePanel<ArtifactMap, ValidFileTypes>
    ): void {
      this.$emit(
        "change",
        this.panels.map((a, currentIndex) => (currentIndex === i ? panel : a))
      );
    },
    /**'
     * Closes the panel if its valid, otherwise opens the panel.
     * @param i - The panel index.
     * @param isValid - Whether the panel is valid.
     */
    handleValidateChange(i: number, isValid: boolean): void {
      if (isValid) {
        this.openPanelIndexes = this.openPanelIndexes.filter(
          (panelIndex) => panelIndex !== i
        );
      } else {
        this.openPanelIndexes.push(i);
      }
    },
    /**
     * Emits changes when a panel is deleted.
     * @param i - The index of the deleted panel.
     */
    handleDeleteFile(i: number): void {
      this.$emit(
        "change",
        this.panels.filter((f, index) => index !== i)
      );
      if (this.panels.length === 0) {
        this.$emit("upload:invalid");
      }
    },
    /**
     * Emits changes when a panel is added.
     * @param payload - The added panel artifact name or trace link.
     */
    handleAddFile(payload: string | Link): void {
      const newPanel = this.uploader.createNewPanel(payload);
      this.$emit("change", this.panels.concat([newPanel]));
      this.openPanelIndexes.push(this.panels.length - 1);
    },
  },
});
</script>
