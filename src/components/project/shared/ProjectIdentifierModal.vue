<template>
  <generic-modal
    :is-open="isOpen"
    :title="title"
    size="m"
    :actions-height="isUploadOpen ? 0 : 50"
    :is-loading="isLoading"
    @close="onClose"
  >
    <template v-slot:body>
      <project-identifier-input
        v-bind:name.sync="name"
        v-bind:description.sync="description"
      />
      <v-switch
        style="margin-left: 80px"
        v-if="doShowUpload"
        v-model="isUploadOpen"
        label="Upload Flat Files"
      />
      <project-files-input
        v-if="doShowUpload && isUploadOpen"
        v-bind:name.sync="name"
        v-bind:description.sync="description"
      />
    </template>
    <template v-slot:actions v-if="!isUploadOpen">
      <v-btn
        @click="onSave"
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
      name: "",
      description: "",
      identifier: createProjectIdentifier(this.project),
      isUploadOpen: false,
    };
  },
  watch: {
    isOpen(isOpen: boolean) {
      if (isOpen) {
        this.identifier = createProjectIdentifier(this.project);
      }
    },
  },
  methods: {
    onClose() {
      this.$emit("close");
    },
    onSave() {
      this.$emit("save", this.identifier);
    },
  },
  computed: {
    isDisabled(): boolean {
      return this.name.length === 0 || (this.doShowUpload && this.isUploadOpen);
    },
  },
});
</script>
