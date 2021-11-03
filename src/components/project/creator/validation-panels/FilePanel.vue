<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <v-container>
        <v-row>
          <v-col cols="1" align-self="center">
            <v-icon :color="getIconColor(iconName)">{{ iconName }}</v-icon>
          </v-col>
          <v-col cols="11" align-self="center">
            <slot name="title" />
          </v-col>
        </v-row>
      </v-container>
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-container>
        <v-row>
          <v-container>
            <v-row style="width: 100%">
              <slot name="before-rows" />
            </v-row>
            <v-row>
              <v-divider />
            </v-row>
          </v-container>
        </v-row>

        <v-row v-if="showFileUploader">
          <v-container class="mt-2">
            <v-row><h4>File:</h4> </v-row>
            <v-row>
              <GenericFileSelector
                :multiple="false"
                @onChangeFiles="emitChangeFiles"
              />
            </v-row>
          </v-container>
        </v-row>

        <GenericSwitch
          v-if="showFileUploader"
          v-model="ignoreErrors"
          label="Ignore Errors"
        />

        <v-row v-if="!isValid && showFileUploader" justify="center">
          <label class="text-caption" style="color: red"> {{ error }}</label>
        </v-row>

        <v-row justify="center">
          <v-expansion-panels accordion>
            <v-expansion-panel v-if="entityNames.length !== 0">
              <v-expansion-panel-header>
                <h4>Entities</h4>
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-row>
                  <v-btn
                    fab
                    x-small
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
              <v-expansion-panel-header>
                <h4>
                  <v-icon small :color="getIconColor(errorIconName)">{{
                    errorIconName
                  }}</v-icon
                  >{{ errors.length === 0 ? "No Errors" : "Errors" }}
                </h4>
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-container>
                  <v-row v-for="(error, i) in errors" :key="i">
                    <v-col align-self="center" class="ma-0 pa-0">
                      {{ i }}:
                      <label class="text-caption" style="color: red">{{
                        error
                      }}</label>
                    </v-col>
                  </v-row>
                </v-container>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-row>

        <v-row v-if="showFileUploader">
          <v-divider />
        </v-row>

        <v-row class="mt-5 mb-5" justify="center">
          <v-btn
            @click="$emit('onDelete')"
            small
            color="error"
            class="pa-2 ma-2"
          >
            Delete
          </v-btn>
        </v-row>
      </v-container>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import GenericFileSelector from "@/components/common/generic/GenericFileSelector.vue";
import { appModule } from "@/store";
import GenericSwitch from "@/components/common/generic/GenericSwitch.vue";

const DEFAULT_ERROR_MESSAGE = "No file has been uploaded.";

export default Vue.extend({
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
    ignoreErrorsFlag: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      error: this.showFileUploader ? DEFAULT_ERROR_MESSAGE : "",
    };
  },
  computed: {
    ignoreErrors: {
      get(): boolean {
        return this.ignoreErrorsFlag;
      },
      set(ignoreErrors: boolean): void {
        this.$emit("update:ignoreErrorsFlag", ignoreErrors);
      },
    },
    isValid(): boolean {
      return (
        this.ignoreErrors ||
        (this.error === "" && this.errors.length === 0) ||
        !this.showFileUploader
      );
    },
    iconName(): string {
      return this.isValid ? "mdi-check" : "mdi-close";
    },
    errorIconName(): string {
      return this.errors.length > 0 ? "mdi-close" : "mdi-check";
    },
  },
  watch: {
    isValid(): void {
      this.$emit("onValidate", this.isValid);
    },
  },
  methods: {
    getIconColor(iconName: string): string {
      switch (iconName) {
        case "mdi-close":
          return "error";
        case "mdi-check":
          return "success";
        default:
          return "primary";
      }
    },
    onClear(): void {
      this.$emit("onChange", undefined);
    },
    emitChangeFiles(file: File): void {
      const fileIsEmpty = file === null;
      if (this.fileRequired) {
        this.error = fileIsEmpty ? DEFAULT_ERROR_MESSAGE : "";
      }
      if (fileIsEmpty) {
        this.onClear();
      } else {
        this.$emit("onChange", file);
      }
    },
    underDevelopmentError(): void {
      appModule.onWarning("Viewing parsed entities is under development.");
    },
  },
});
</script>
