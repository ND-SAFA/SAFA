<template>
  <flex-box
    v-if="isOpen"
    align="center"
    justify="space-between"
    full-width
    y="3"
  >
    <flex-box>
      <button-row :definitions="[sourceDefinition]" />
      <v-icon class="mx-2">mdi-arrow-right</v-icon>
      <button-row :definitions="[targetDefinition]" />
    </flex-box>
    <v-btn @click="handleSubmit" color="primary" class="ml-10">
      Create Trace Matrix
    </v-btn>
  </flex-box>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ButtonDefinition, ButtonType, Link, TraceFile } from "@/types";
import { logModule } from "@/store";
import { ButtonRow, FlexBox } from "@/components/common";

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
    ButtonRow,
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
      if (this.source === "" || this.target === "") {
        logModule.onWarning(
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
      } as Link);
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
     * Returns all target artifact types.
     */
    targetTypes(): string[] {
      if (this.source === "") {
        return [];
      }

      const traceIds = this.traceFiles.map(
        (f) => `${f.sourceId}-${f.targetId}`
      );

      return this.artifactTypes.filter((t) => {
        const currentTraceId = `${this.source}-${t}`;
        return !traceIds.includes(currentTraceId);
      });
    },
    /**
     * Defines the source button.
     */
    sourceDefinition(): ButtonDefinition {
      return {
        type: ButtonType.LIST_MENU,
        label: this.source === "" ? "Select Source" : this.source,
        menuItems: this.artifactTypes.map((type) => ({
          name: type,
          onClick: () => (this.source = type),
        })),
        buttonColor: "primary",
        buttonIsText: false,
        showSelectedValue: true,
      };
    },
    /**
     * Defines the target button.
     */
    targetDefinition(): ButtonDefinition {
      return {
        type: ButtonType.LIST_MENU,
        label: this.target === "" ? "Select Target" : this.target,
        menuItems: this.targetTypes.map((type) => ({
          name: type,
          onClick: () => (this.target = type),
        })),
        buttonColor: "primary",
        buttonIsText: false,
        showSelectedValue: true,
        isDisabled: this.targetTypes.length === 0,
      };
    },
  },
});
</script>
