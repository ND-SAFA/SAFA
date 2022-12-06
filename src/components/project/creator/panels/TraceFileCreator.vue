<template>
  <flex-box v-if="isOpen" align="start" justify="center" full-width y="3">
    <v-select
      filled
      label="Source Type"
      v-model="source"
      :items="artifactTypes"
      data-cy="input-source-type"
    />
    <v-icon class="mx-2 mt-5">mdi-arrow-right</v-icon>
    <v-select
      filled
      label="Target Type"
      v-model="target"
      :items="artifactTypes"
      data-cy="input-target-type"
    />
    <v-btn
      :disabled="disabled"
      @click="handleSubmit"
      color="primary"
      class="ml-10 mt-3"
      data-cy="button-create-trace-matrix"
    >
      Create Trace Matrix
    </v-btn>
  </flex-box>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { LinkSchema, TraceFile } from "@/types";
import { logStore } from "@/hooks";
import { FlexBox } from "@/components/common";

/**
 * Trace file creator.
 *
 * @emits-1 `close` - On close.
 * @emits-2 `submit` ({ source: string, target: string }) - On submit.
 */
export default Vue.extend({
  name: "TraceFileCreator",
  components: {
    FlexBox,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    traceFiles: {
      type: Array as PropType<TraceFile[]>,
      required: true,
    },
    artifactTypes: {
      type: Array as PropType<string[]>,
      required: true,
    },
  },
  data() {
    return {
      source: "",
      target: "",
    };
  },
  methods: {
    /**
     * Attempts to create a new trace file panel.
     */
    handleSubmit(): void {
      if (this.disabled) {
        logStore.onWarning(
          "Please select valid source and target artifact types."
        );
        return;
      }

      this.$emit("close");
      this.$emit("submit", {
        sourceName: this.source,
        sourceId: this.source,
        targetName: this.target,
        targetId: this.target,
      } as LinkSchema);
    },
  },
  watch: {
    /**
     * Resets trace direction data when opened.
     */
    isOpen(open: boolean): void {
      if (!open) return;

      this.source = "";
      this.target = "";
    },
  },
  computed: {
    /**
     * @return Whether this matrix creation is disabled.
     */
    disabled(): boolean {
      return this.source === "" || this.target === "";
    },
  },
});
</script>
