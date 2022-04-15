<template>
  <generic-modal
    size="md"
    :is-open="isOpen"
    :title="title"
    @close="handleCancel"
  >
    <template v-slot:body>
      <v-text-field
        v-model="confirmText"
        :label="textboxLabel"
        class="ma-3"
        filled
      />
    </template>
    <template v-slot:actions>
      <v-btn
        :disabled="!validated"
        color="error"
        @click="handleConfirm"
        class="ml-auto"
      >
        Delete
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import { ProjectIdentifier } from "@/types";
import Vue, { PropType } from "vue";
import { GenericModal } from "@/components/common";

/**
 * A modal for confirming project deletion.
 *
 * @emits-1 `confirm` (string) - On delete confirm.
 * @emits-2 `cancel` - On delete cancel.
 */
export default Vue.extend({
  components: { GenericModal },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    project: {
      type: Object as PropType<ProjectIdentifier>,
      required: false,
    },
  },
  data() {
    return {
      confirmText: "",
      textboxLabel: "",
      title: "",
      validated: false,
    };
  },
  methods: {
    clearData(): void {
      this.confirmText = "";
      this.validated = false;
    },
    handleConfirm() {
      const project = this.$props.project;
      if (this.validated) {
        this.$emit("confirm", project);
      }
    },
    handleCancel() {
      this.$emit("cancel");
    },
  },
  watch: {
    project(project: ProjectIdentifier) {
      if (project !== undefined) {
        this.textboxLabel = `Type "${project.name}"`;
        this.title = `Deleting: ${project.name}`;
      }
    },
    confirmText() {
      const project = this.$props.project;
      if (project !== undefined) {
        if (this.confirmText === project.name) {
          this.validated = true;
          return;
        }
      }
      this.validated = false;
    },
    isOpen(isOpen: boolean) {
      if (isOpen) {
        this.clearData();
      }
    },
  },
});
</script>
