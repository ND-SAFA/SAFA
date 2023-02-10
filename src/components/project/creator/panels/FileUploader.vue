<template>
  <v-container>
    <file-format-alert />
    <validated-panels
      :item-name="itemName"
      :show-error="showError"
      :is-valid-states="isValidStates"
      :is-button-disabled="isCreatorOpen"
      :default-valid-state="defaultValidState"
      @add="isCreatorOpen = true"
      @upload:valid="$emit('upload:valid')"
      @upload:invalid="$emit('upload:invalid')"
    >
      <template #panels>
        <v-expansion-panels v-model="openPanelIndexes" multiple>
          <file-panel-controller
            v-for="(panel, i) in uploader.panels"
            :key="panel.title"
            :panel="panel"
            :artifact-map="artifactMap"
            @change="handleChange(i, $event)"
            @delete="handleDeleteFile(i)"
            @validate="handleValidateChange(i, $event)"
          />
        </v-expansion-panels>
        <slot
          name="creator"
          :isCreatorOpen="isCreatorOpen"
          :onAddFile="handleAddFile"
          :onClose="handleCloseCreator"
        />
      </template>
    </validated-panels>
  </v-container>
</template>

<script lang="ts">
/**
 * A generic file uploader.
 */
export default {
  name: "FileUploader",
};
</script>

<script setup lang="ts">
import { computed, ref, defineProps, defineEmits } from "vue";
import {
  LinkSchema,
  ArtifactMap,
  ParseFilePanel,
  FileUploader,
  ValidFileTypes,
  ValidPayloads,
} from "@/types";
import { FileFormatAlert } from "@/components/common";
import FilePanelController from "./FilePanelController.vue";
import ValidatedPanels from "./ValidatedPanels.vue";

const props = defineProps<{
  itemName: string;
  artifactMap: ArtifactMap;
  uploader: FileUploader<ArtifactMap, ValidPayloads, ValidFileTypes>;
  defaultValidState?: boolean;
}>();

const emit = defineEmits<{
  (e: "change", panels: ParseFilePanel<ArtifactMap, ValidFileTypes>[]): void;
  (e: "upload:valid"): void;
  (e: "upload:invalid"): void;
}>();

const isCreatorOpen = ref(false);
const openPanelIndexes = ref<number[]>([]);

const projectFiles = computed(() =>
  props.uploader.panels.map((p) => p.projectFile)
);
const isValidStates = computed(() =>
  props.uploader.panels.map((p) => p.projectFile.isValid)
);
const showError = computed(() =>
  props.defaultValidState ? false : projectFiles.value.length === 0
);

/**
 * Closes the creator.
 */
function handleCloseCreator(): void {
  isCreatorOpen.value = false;
}

/**
 * Emits changed panels.
 */
function handleChange(
  i: number,
  panel: ParseFilePanel<ArtifactMap, ValidFileTypes>
): void {
  emit(
    "change",
    props.uploader.panels.map((a, currentIndex) =>
      currentIndex === i ? panel : a
    )
  );
}

/**
 * Closes the panel if its valid, otherwise opens the panel.
 * @param i - The panel index.
 * @param isValid - Whether the panel is valid.
 */
function handleValidateChange(i: number, isValid: boolean): void {
  if (isValid) {
    openPanelIndexes.value = openPanelIndexes.value.filter(
      (panelIndex) => panelIndex !== i
    );
  } else {
    openPanelIndexes.value.push(i);
  }
}

/**
 * Emits changes when a panel is deleted.
 * @param i - The index of the deleted panel.
 */
function handleDeleteFile(i: number): void {
  emit(
    "change",
    props.uploader.panels.filter((f, index) => index !== i)
  );
  if (props.uploader.panels.length === 0) {
    emit("upload:invalid");
  }
}

/**
 * Emits changes when a panel is added.
 * @param payload - The added panel artifact name or trace link.
 */
function handleAddFile(payload: string | LinkSchema): void {
  const newPanel = props.uploader.createNewPanel(payload);
  const updatedPanels = [...props.uploader.panels, newPanel];

  openPanelIndexes.value.push(updatedPanels.length - 1);
  emit("change", updatedPanels);
}
</script>
