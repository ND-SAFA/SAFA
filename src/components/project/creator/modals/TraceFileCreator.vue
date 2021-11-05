<template>
  <GenericModal
    title="Create Trace Links"
    :isOpen="isOpen"
    @onClose="$emit('onClose')"
    size="s"
  >
    <template v-slot:body>
      <v-container>
        <v-row>
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
      </v-container>
    </template>

    <template v-slot:actions>
      <v-row justify="center">
        <v-btn @click="onSubmit" small color="primary">Create</v-btn>
      </v-row>
    </template>
  </GenericModal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import GenericModal from "@/components/common/generic/GenericModal.vue";
import ButtonRow from "@/components/common/button-row/ButtonRow.vue";
import { ButtonDefinition, ButtonType, TraceFile } from "@/types";
import { appModule } from "@/store";

export default Vue.extend({
  components: {
    GenericModal,
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
