<template>
  <v-row
    v-if="isOpen"
    align="center"
    class="mx-auto my-3"
    style="max-width: 35em"
  >
    <v-row align="start">
      <v-col align-self="center">
        <ButtonRow :definitions="[sourceDefinition]"
      /></v-col>
      <v-col align-self="center">
        <v-row justify="center">
          <v-icon>mdi-arrow-right</v-icon>
        </v-row>
      </v-col>
      <v-col align-self="center">
        <ButtonRow :definitions="[targetDefinition]" />
      </v-col>
    </v-row>
    <v-btn @click="onSubmit" color="primary" class="ml-10"> Create </v-btn>
  </v-row>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ButtonDefinition, ButtonType, TraceFile } from "@/types";
import { appModule } from "@/store";
import { ButtonRow } from "@/components/common";

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
        this.$emit("onSubmit", { source: this.source, target: this.target });
        this.$emit("onClose");
      } else {
        appModule.onWarning(
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
