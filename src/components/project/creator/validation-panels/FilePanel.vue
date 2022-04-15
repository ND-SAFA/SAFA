<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <v-row dense align="center" justify="start">
        <v-col class="flex-grow-0">
          <v-icon :color="iconColor">{{ iconName }}</v-icon>
        </v-col>
        <v-col>
          <slot name="title" />
        </v-col>
      </v-row>
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-container>
        <v-row>
          <v-container>
            <v-row class="full-width">
              <slot name="before-rows" />
            </v-row>
            <v-row>
              <v-divider />
            </v-row>
          </v-container>
        </v-row>

        <v-row v-if="showFileUploader">
          <generic-file-selector
            :multiple="false"
            @change:files="emitChangeFiles"
          />
        </v-row>

        <v-row justify="space-between" align="center" dense>
          <v-col>
            <generic-switch
              v-if="showFileUploader"
              v-model="ignoreErrors"
              label="Ignore Errors"
            />
          </v-col>
          <v-col v-if="!isValid && showFileUploader" style="text-align: end">
            {{ error }}
          </v-col>
        </v-row>

        <v-row justify="center">
          <v-expansion-panels accordion>
            <v-expansion-panel v-if="entityNames.length !== 0">
              <v-expansion-panel-header>
                <span class="text-h6">Entities</span>
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-row>
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
                </v-row>
              </v-expansion-panel-content>
            </v-expansion-panel>
            <v-expansion-panel v-if="errors.length > 0">
              <v-expansion-panel-header disable-icon-rotate>
                <span class="text-h6">
                  {{ errors.length === 0 ? "No Errors" : "Errors" }}
                </span>
                <template v-slot:actions>
                  <v-icon color="error">mdi-alert-circle</v-icon>
                </template>
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <p
                  v-for="(error, i) in errors"
                  :key="i"
                  class="error--text my-0"
                >
                  {{ error }}
                </p>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-row>

        <v-row v-if="showFileUploader">
          <v-divider />
        </v-row>

        <v-row class="mt-5" justify="end">
          <v-btn @click="$emit('delete')" color="error"> Delete </v-btn>
        </v-row>
      </v-container>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { logModule } from "@/store";
import { GenericSwitch, GenericFileSelector } from "@/components/common";

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
      logModule.onWarning("Viewing parsed entities is under development.");
    },
  },
});
</script>
