<template>
  <v-expansion-panel data-cy="panel-files" class="primary-border">
    <v-expansion-panel-title>
      <flex-box align="center">
        <v-progress-circular v-if="isLoading" indeterminate class="mr-2" />
        <v-icon v-else class="mr-1" :color="iconColor">
          {{ iconName }}
        </v-icon>
        <slot name="title" />
      </flex-box>
    </v-expansion-panel-title>
    <v-expansion-panel-text>
      <slot name="before-rows" />

      <file-input
        v-if="showFileUploader"
        :multiple="false"
        data-cy="input-files-panel"
        @input="emitChangeFiles"
      />

      <flex-box justify="space-between" align="center">
        <switch-input
          v-if="showFileUploader"
          v-model="ignoreErrors"
          label="Ignore Errors"
          data-cy="button-ignore-errors"
        />
        <typography
          v-if="!isValid && showFileUploader"
          error
          :value="errorMessage"
        />
      </flex-box>

      <v-expansion-panels accordion>
        <v-expansion-panel v-if="entityNames.length !== 0">
          <v-expansion-panel-title data-cy="button-file-entities">
            <typography variant="subtitle" value="Entities" />
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-btn
              v-for="entityName in entityNames"
              :key="entityName"
              outlined
              color="primary"
              class="ma-1"
              data-cy="button-created-entity"
              @click="underDevelopmentError"
            >
              {{ entityName }}
            </v-btn>
          </v-expansion-panel-text>
        </v-expansion-panel>
        <v-expansion-panel v-if="errors.length > 0">
          <v-expansion-panel-title disable-icon-rotate>
            <typography
              variant="subtitle"
              :value="errors.length === 0 ? 'No Errors' : 'Errors'"
            />
            <template #actions>
              <v-icon color="error">mdi-alert-circle</v-icon>
            </template>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <typography
              v-for="(error, i) in errors"
              :key="i"
              error
              :value="error"
            />
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>

      <flex-box justify="space-between" t="4">
        <v-spacer />
        <v-btn
          color="error"
          data-cy="button-delete-artifact"
          @click="emit('delete')"
        >
          Delete
        </v-btn>
      </flex-box>
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>

<script lang="ts">
/**
 * Displays a file panel.
 */
export default {
  name: "FilePanel",
};
</script>

<script setup lang="ts">
import {
  computed,
  ref,
  watch,
  withDefaults,
  defineEmits,
  defineProps,
} from "vue";
import { logStore, useVModel } from "@/hooks";
import {
  SwitchInput,
  FileInput,
  Typography,
  FlexBox,
} from "@/components/common";

const DEFAULT_ERROR_MESSAGE = "No file has been uploaded.";

const props = withDefaults(
  defineProps<{
    entityNames: string[];
    errors: string[];
    ignoreErrors: boolean;
    isLoading: boolean;
    showFileUploader?: boolean;
    fileRequired?: boolean;
    entitiesAreFab?: boolean;
  }>(),
  { showFileUploader: true, fileRequired: true, entitiesAreFab: true }
);

const emit = defineEmits<{
  (e: "update:ignoreErrors", value: boolean): void;
  (e: "validate", isValue: boolean): void;
  (e: "change", file: File | null): void;
  (e: "delete"): void;
}>();

const errorMessage = ref(props.showFileUploader ? DEFAULT_ERROR_MESSAGE : "");
const ignoreErrors = useVModel(props, "ignoreErrors");

const isValid = computed(
  () =>
    ignoreErrors.value ||
    (errorMessage.value === "" && props.errors.length === 0) ||
    !props.showFileUploader
);

const iconName = computed(() => (isValid.value ? "mdi-check" : "mdi-close"));
const iconColor = computed(() => (isValid.value ? "success" : "error"));

/**
 * Emits a change when the panel is cleared.
 */
function handleClear(): void {
  emit("change", null);
}

/**
 * Emits changed files.
 * @param file - The uploaded file.
 */
function emitChangeFiles(file: File | null): void {
  const fileIsEmpty = file === null;

  if (props.fileRequired) {
    errorMessage.value = fileIsEmpty ? DEFAULT_ERROR_MESSAGE : "";
  }

  if (fileIsEmpty) {
    handleClear();
  } else {
    emit("change", file);
  }
}

function underDevelopmentError(): void {
  logStore.onInfo("Viewing parsed entities is under development.");
}

watch(
  () => isValid.value,
  () => emit("validate", isValid.value)
);
</script>
