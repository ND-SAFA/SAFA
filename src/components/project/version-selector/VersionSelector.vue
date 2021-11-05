<template>
  <GenericSelector
    itemKey="versionId"
    noDataText="Project contains no versions"
    :headers="headers"
    :items="versions"
    :isOpen="isOpen"
    :isLoading="isLoading"
    :hasEdit="false"
    @onSelectItem="selectItem"
    @onDeleteItem="deleteItem"
    @onAddItem="addItem"
    @onRefresh="refresh"
  >
    <template v-slot:addItemDialogue>
      <VersionCreator
        :isOpen="addVersionDialogue"
        :project="project"
        @onClose="onCreatorClose"
        @onCreate="onVersionCreated"
      />
    </template>
    <template v-slot:deleteItemDialogue>
      <ConfirmVersionDelete
        :version="versionToDelete"
        :deleteDialogue="deleteVersionDialogue"
        @onCancelDelete="cancelDelete"
        @onConfirmDelete="confirmDelete"
      />
    </template>
  </GenericSelector>
</template>

<script lang="ts">
import { ProjectIdentifier, ProjectVersion } from "@/types";
import GenericSelector from "@/components/common/generic/GenericSelector.vue";
import Vue, { PropType } from "vue";
import { deleteProjectVersion, getProjectVersions } from "@/api/project-api";
import VersionCreator from "@/components/project/version-selector/VersionCreator.vue";
import ConfirmVersionDelete from "@/components/project/version-selector/ConfirmVersionDelete.vue";
import { DataItem } from "@/types";
import { versionSelectorHeader } from "@/components/project/version-selector/headers";
import { appModule } from "@/store";

export default Vue.extend({
  components: { GenericSelector, VersionCreator, ConfirmVersionDelete },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    project: {
      type: Object as PropType<ProjectIdentifier>,
      required: true,
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
