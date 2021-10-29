<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <v-container>
        <v-row>
          <v-col cols="1" align-self="center">
            <v-icon :color="iconColor">{{ iconName }}</v-icon>
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
          <slot name="before-rows" />
        </v-row>

        <v-row v-if="showFileUploader">
          <v-container>
            <v-row><h4>File:</h4> </v-row>
            <v-row>
              <GenericFileSelector
                :multiple="false"
                @onChangeFiles="emitChangeFiles"
                @onClear="$emit('onChange', undefined)"
              />
            </v-row>
          </v-container>
        </v-row>
        <v-row v-if="!isValid && showFileUploader" justify="center">
          <label class="text-caption" style="color: red"> {{ error }}</label>
        </v-row>

        <v-row>
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
import Vue from "vue";
import GenericFileSelector from "@/components/common/generic/GenericFileSelector.vue";

const DEFAULT_ERROR_MESSAGE = "No file has been uploaded.";

export default Vue.extend({
  components: {
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
  },
  data() {
    return {
      error: DEFAULT_ERROR_MESSAGE,
    };
  },
  computed: {
    isValid(): boolean {
      return this.error === "" || !this.showFileUploader;
    },
    iconName(): string {
      return this.isValid ? "mdi-check" : "mdi-close";
    },
    iconColor(): string {
      return this.isValid ? "success" : "error";
    },
  },
  methods: {
    emitChangeFiles(file: File): void {
      const fileIsEmpty = file === null;
      if (this.fileRequired) {
        this.error = fileIsEmpty ? DEFAULT_ERROR_MESSAGE : "";
      }
      if (fileIsEmpty) {
        this.$emit("onChange", undefined);
      } else {
        this.$emit("onChange", file);
      }
    },
  },
});
</script>
