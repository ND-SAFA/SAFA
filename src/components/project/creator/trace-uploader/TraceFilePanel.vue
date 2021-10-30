<template>
  <FilePanel
    @onChange="onChange"
    @onDelete="$emit('onDelete')"
    :showFileUploader="!traceFile.isGenerated"
    :errors="errors"
  >
    <template v-slot:title>
      <label>
        {{ traceFile.source }}
      </label>
      <v-icon>mdi-arrow-right</v-icon>
      <label>
        {{ traceFile.target }}
      </label>
    </template>

    <template v-slot:before-rows>
      <v-row>
        <v-col cols="9" align-self="center"> Generate Links: </v-col>
        <v-col cols="3" align-self="center">
          <v-switch v-model="traceFile.isGenerated" />
        </v-col>
      </v-row>
    </template>

    <template v-slot:after-rows>
      <v-container>
        <v-row><h4>Parsed Traces</h4> </v-row>
        <v-row v-if="traceFile.traces !== undefined">
          <v-btn
            x-small
            color="primary"
            class="ma-1"
            v-for="trace in traceFile.traces"
            :key="`${trace.source}-${trace.target}`"
            @click="underDevelopmentError()"
          >
            {{ trace.source }}-{{ trace.target }}
          </v-btn>
        </v-row>
        <v-row v-else>
          <label class="text-caption">
            No trace links have been parseed.
          </label>
        </v-row>
      </v-container>
    </template>
  </FilePanel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TraceFile } from "@/types/common-components";
import FilePanel from "@/components/project/creator/shared/FilePanel.vue";

export default Vue.extend({
  components: {
    FilePanel,
  },
  props: {
    traceFile: {
      type: Object as PropType<TraceFile>,
      required: true,
    },
  },

  computed: {
    isValid(): boolean {
      return this.traceFile.file !== undefined || this.traceFile.isGenerated;
    },
    errors(): string[] {
      return this.traceFile.errors === undefined ? [] : this.traceFile.errors;
    },
  },
  methods: {
    onChange(file: File | undefined): void {
      this.$emit("onChange", { ...this.traceFile, file });
    },
    emitValidationState(): void {
      if (this.isValid) {
        this.$emit("onIsValid");
      } else {
        this.$emit("onIsInvalid");
      }
    },
  },
  watch: {
    isValid(): void {
      this.emitValidationState();
    },
  },
  mounted() {
    this.emitValidationState();
  },
});
</script>
