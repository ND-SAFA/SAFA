<template>
  <v-row v-if="isOpen" class="my-3" align="center">
    <v-col cols="10">
      <div class="d-flex" style="width: min-content">
        <button-row :definitions="[sourceDefinition]" />
        <v-icon class="mx-2">mdi-arrow-right</v-icon>
        <button-row :definitions="[targetDefinition]" />
      </div>
    </v-col>
    <v-col cols="2">
      <v-btn @click="onSubmit" color="primary" class="ml-10">Create Link</v-btn>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ButtonDefinition, ButtonType, Link, TraceFile } from "@/types";
import { logModule } from "@/store";
import { ButtonRow } from "@/components/common";

/**
 * Trace file creator.
 *
 * @emits-1 `close` - On close.
 * @emits-2 `submit` ({ source: string, target: string }) - On submit.
 */
export default Vue.extend({
  components: {
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
    onSubmit(): void {
      if (this.source !== "" && this.target !== "") {
        const traceLink: Link = {
          sourceName: this.source,
          sourceId: this.source,
          targetName: this.target,
          targetId: this.target,
        };
        this.$emit("submit", traceLink);
        this.$emit("close");
      } else {
        logModule.onWarning(
          "Please select valid source and target artifact types."
        );
      }
    },
  },
  watch: {
    isOpen(isOpen: boolean): void {
      if (isOpen) {
        this.source = "";
        this.target = "";
      }
    },
  },
  computed: {
    targetTypes(): string[] {
      const traceIds = this.traceFiles.map((f) => `${f.source}-${f.target}`);
      if (this.source === "") {
        return [];
      } else {
        return this.artifactTypes.filter((t) => {
          const currentTraceId = `${this.source}-${t}`;
          return !traceIds.includes(currentTraceId);
        });
      }
    },
    sourceDefinition(): ButtonDefinition {
      return {
        type: ButtonType.LIST_MENU,
        label: this.source === "" ? "Select Source" : this.source,
        menuItems: this.artifactTypes,
        menuHandlers: this.artifactTypes.map(
          (type) => () => (this.source = type)
        ),
        buttonColor: "primary",
        buttonIsText: false,
        showSelectedValue: true,
      };
    },
    targetDefinition(): ButtonDefinition {
      return {
        type: ButtonType.LIST_MENU,
        label: this.target === "" ? "Select Target" : this.target,
        menuItems: this.targetTypes,
        menuHandlers: this.targetTypes.map(
          (type) => () => (this.target = type)
        ),
        buttonColor: "primary",
        buttonIsText: false,
        showSelectedValue: true,
        isDisabled: this.targetTypes.length === 0,
      };
    },
  },
});
</script>
