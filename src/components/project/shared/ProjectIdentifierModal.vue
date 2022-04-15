<template>
  <generic-modal
    :is-open="isOpen"
    :title="title"
    size="m"
    :actions-height="isUploadOpen ? 0 : 50"
    :is-loading="isLoading"
    @close="handleClose"
  >
    <template v-slot:body>
      <project-identifier-input
        v-bind:name.sync="identifier.name"
        v-bind:description.sync="identifier.description"
      />
      <v-switch
        style="margin-left: 80px"
        v-if="doShowUpload"
        v-model="isUploadOpen"
        label="Upload Flat Files"
      />
      <project-files-input
        v-if="doShowUpload && isUploadOpen"
        v-bind:name.sync="identifier.name"
        v-bind:description.sync="identifier.description"
      />
    </template>
    <template v-slot:actions v-if="!isUploadOpen">
      <v-btn
        @click="handleSave"
        color="primary"
        class="ml-auto"
        :disabled="isDisabled"
      >
        <v-icon>mdi-check</v-icon>
        Save
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ProjectIdentifier } from "@/types";
import { createProjectIdentifier } from "@/util";
import { GenericModal } from "@/components/common";
import ProjectIdentifierInput from "./ProjectIdentifierInput.vue";
import ProjectFilesInput from "./ProjectFilesInput.vue";

/**
 * A modal for renaming a project.
 *
 * @emits-1 `close` - On close.
 * @emits-2 `save` (ProjectIdentifier) - On project save.
 */
export default Vue.extend({
  name: "ProjectIdentifierModal",
  components: {
    GenericModal,
    ProjectIdentifierInput,
    ProjectFilesInput,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    project: {
      type: Object as PropType<ProjectIdentifier>,
      required: false,
    },
    title: {
      type: String,
      required: true,
    },
    isLoading: {
      type: Boolean,
      required: false,
      default: false,
    },
    doShowUpload: Boolean,
  },
  data() {
    return {
      identifier: createProjectIdentifier(this.project),
      isUploadOpen: false,
      isDisabled: true,
    };
  },
  watch: {
    /**
     * Resets identifier data when opened.
     */
    isOpen(open: boolean) {
      if (!open) return;

      this.identifier = createProjectIdentifier(this.project);
    },
    /**
     * Verified fields when the identifier changes.
     */
    identifier: {
      deep: true,
      handler() {
        this.isDisabled =
          this.identifier.name.length === 0 ||
          (this.doShowUpload && this.isUploadOpen);
      },
    },
  },
  methods: {
    /**
     * Emits a request to close.
     */
    handleClose() {
      this.$emit("close");
    },
    /**
     * Emits a request to save a project.
     */
    handleSave() {
      this.$emit("save", this.identifier);
    },
  },
});
</script>
