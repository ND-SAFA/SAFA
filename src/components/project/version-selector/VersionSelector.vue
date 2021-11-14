<template>
  <generic-selector
    v-if="this.isOpen"
    item-key="versionId"
    no-data-text="Project contains no versions"
    :headers="headers"
    :items="versions"
    :is-open="isOpen"
    :is-loading="isLoading"
    :has-edit="false"
    @select-item="selectItem"
    @delete-item="deleteItem"
    @add-item="addItem"
    @refresh="refresh"
  >
    <template v-slot:addItemDialogue>
      <version-creator
        :is-open="addVersionDialogue"
        :project="project"
        @onClose="onCreatorClose"
        @onCreate="onVersionCreated"
      />
    </template>
    <template v-slot:deleteItemDialogue>
      <confirm-version-delete
        :version="versionToDelete"
        :delete-dialogue="deleteVersionDialogue"
        @onCancelDelete="cancelDelete"
        @onConfirmDelete="confirmDelete"
      />
    </template>
  </generic-selector>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ProjectIdentifier, ProjectVersion, DataItem } from "@/types";
import { deleteProjectVersion, getProjectVersions } from "@/api";
import { appModule } from "@/store";
import { GenericSelector } from "@/components/common";
import { versionSelectorHeader } from "./headers";
import VersionCreator from "./VersionCreator.vue";
import ConfirmVersionDelete from "./ConfirmVersionDelete.vue";

export default Vue.extend({
  components: { GenericSelector, VersionCreator, ConfirmVersionDelete },
  props: {
    /**
     * Whether this selector is currently open and in view. Note, if within
     * a stepper modal, isOpen is true only when the this component is within
     * the current step.
     */
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
      headers: versionSelectorHeader,
      versions: [] as ProjectVersion[],
      versionToDelete: undefined as ProjectVersion | undefined,
      deleteVersionDialogue: false,
      addVersionDialogue: false,
      isLoading: false,
    };
  },
  mounted() {
    this.loadItems();
  },
  watch: {
    project() {
      this.loadItems();
    },
  },
  methods: {
    onCreatorClose() {
      this.addVersionDialogue = false;
    },
    refresh() {
      this.loadItems();
    },
    selectItem(item: DataItem<ProjectVersion>) {
      if (item.value) {
        this.$emit("onVersionSelected", item.item);
      } else {
        this.$emit("onVersionUnselected");
      }
    },
    addItem() {
      this.addVersionDialogue = true;
    },
    deleteItem(version: ProjectVersion) {
      this.versionToDelete = version;
      this.deleteVersionDialogue = true;
    },

    onVersionCreated(version: ProjectVersion) {
      this.versions = [version].concat(this.versions);
      this.addVersionDialogue = false;
      this.$emit("onVersionSelected", version);
    },
    cancelDelete() {
      this.deleteVersionDialogue = false;
    },
    confirmDelete(version: ProjectVersion) {
      this.deleteVersionDialogue = false;
      this.isLoading = true;
      deleteProjectVersion(version.versionId)
        .then(() => {
          appModule.onSuccess("Project version successfully deleted");
          this.versions = this.versions.filter(
            (v) => v.versionId != version.versionId
          );
        })
        .finally(() => (this.isLoading = false));
    },
    loadItems() {
      this.isLoading = true;
      const project: ProjectIdentifier = this.$props.project;
      if (project !== undefined) {
        getProjectVersions(project.projectId)
          .then((versions: ProjectVersion[]) => {
            this.versions = versions;
          })
          .finally(() => {
            this.isLoading = false;
          });
      }
    },
  },
});
</script>
