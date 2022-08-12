<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <flex-box align="center">
        <v-icon
          class="mr-1"
          :color="iconColor"
          data-cy="button-artifact-dropbox"
        >
          {{ iconName }}
        </v-icon>
        <slot name="title" />
      </flex-box>
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <slot name="before-rows" />

      <generic-file-selector
        v-if="showFileUploader"
        :multiple="false"
        @input="emitChangeFiles"
      />

      <flex-box justify="space-between" align="center">
        <generic-switch
          v-if="showFileUploader"
          v-model="ignoreErrors"
          label="Ignore Errors"
          data-cy="button-ignore-errors"
        />
        <typography v-if="!isValid && showFileUploader" error :value="error" />
      </flex-box>

      <v-expansion-panels accordion>
        <v-expansion-panel v-if="entityNames.length !== 0">
          <v-expansion-panel-header data-cy="button-file-entities">
            <typography variant="subtitle" value="Entities" />
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-btn
              outlined
              color="primary"
              class="ma-1"
              v-for="entityName in entityNames"
              :key="entityName"
              @click="underDevelopmentError()"
            >
              {{ entityName }}
            </v-btn>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel v-if="errors.length > 0">
          <v-expansion-panel-header disable-icon-rotate>
            <typography
              variant="subtitle"
              :value="errors.length === 0 ? 'No Errors' : 'Errors'"
            />
            <template v-slot:actions>
              <v-icon color="error">mdi-alert-circle</v-icon>
            </template>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <typography
              v-for="(error, i) in errors"
              :key="i"
              error
              :value="error"
            />
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>

      <flex-box justify="space-between" t="4">
        <v-spacer />
        <v-btn
          @click="$emit('delete')"
          color="error"
          data-cy="button-delete-artifact"
        >
          Delete
        </v-btn>
      </flex-box>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { logModule } from "@/store";
import {
  GenericSwitch,
  GenericFileSelector,
  Typography,
  FlexBox,
} from "@/components/common";

const DEFAULT_ERROR_MESSAGE = "No file has been uploaded.";

/**
 * Displays a file panel.
 *
 * @emits-1 `delete` - On delete.
 * @emits-2 `update:ignore-errors-flag` (ignoreErrors: boolean) - On update ignore errors.
 * @emits-3 `validate` (isValid: boolean) - On validate.
 * @emits-4 `change` (file?: File) - On change.
 */
export default Vue.extend({
  name: "FilePanel",
  components: {
    FlexBox,
    Typography,
    GenericSwitch,
    GenericFileSelector,
  },
  props: {
    fileRequired: {
      type: Boolean,
      default: true,
    },
    showFileUploader: {
      type: Boolean,
      default: true,
    },
    errors: {
      type: Array as PropType<string[]>,
      required: true,
    },
    entityNames: {
      type: Array as PropType<string[]>,
      required: true,
    },
    entitiesAreFab: {
      type: Boolean,
      default: true,
    },
    ignoreErrorsFlag: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      isOpen: true,
      error: this.showFileUploader ? DEFAULT_ERROR_MESSAGE : "",
    };
  },
  computed: {
    /**
     * Emits updates to ignore errors.
     */
    ignoreErrors: {
      get(): boolean {
        return this.ignoreErrorsFlag;
      },
      set(ignoreErrors: boolean): void {
        this.$emit("update:ignore-errors-flag", ignoreErrors);
      },
    },
    /**
     * Whether this file panel is valid.
     */
    isValid(): boolean {
      return (
        this.ignoreErrors ||
        (this.error === "" && this.errors.length === 0) ||
        !this.showFileUploader
      );
    },
    /**
     * The panel's icon.
     */
    iconName(): string {
      return this.isValid ? "mdi-check" : "mdi-close";
    },
    /**
     * The panel's color.
     */
    iconColor(): string {
      return this.isValid ? "success" : "error";
    },
  },
  watch: {
    /**
     * Emit changes to the validation status.
     */
    isValid(): void {
      this.$emit("validate", this.isValid);
    },
  },
  methods: {
    /**
     * Emits a change when the panel is cleared.
     */
    handleClear(): void {
      this.$emit("change", undefined);
    },
    /**
     * Emits changed files.
     * @param file - The uploaded file.
     */
    emitChangeFiles(file: File | null): void {
      const fileIsEmpty = file === null;

      if (this.fileRequired) {
        this.error = fileIsEmpty ? DEFAULT_ERROR_MESSAGE : "";
      }

      if (fileIsEmpty) {
        this.handleClear();
      } else {
        this.$emit("change", file);
      }
    },
    underDevelopmentError(): void {
      logModule.onInfo("Viewing parsed entities is under development.");
    },
  },
});
</script>
