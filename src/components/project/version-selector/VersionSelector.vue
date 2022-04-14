<template>
  <generic-selector
    v-if="this.isOpen"
    item-key="versionId"
    no-data-text="Project contains no versions"
    :headers="headers"
    :items="displayedVersions"
    :is-open="isOpen"
    :is-loading="isLoading"
    :has-edit="false"
    :can-delete-last-item="false"
    @item:select="onSelectVersion"
    @item:delete="onDeleteVersion"
    @item:add="onAddItem"
    @refresh="loadProjectVersions"
  >
    <template v-slot:addItemDialogue>
      <version-creator
        :is-open="addVersionDialogue"
        :project="project"
        @close="onCreatorClose"
        @create="onVersionCreated"
      />
    </template>
    <template v-slot:deleteItemDialogue>
      <confirm-version-delete
        :version="versionToDelete"
        :delete-dialogue="deleteVersionDialogue"
        @cancel="onCancelDeleteVersion"
        @confirm="onConfirmDeleteVersion"
      />
    </template>
  </generic-selector>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ProjectIdentifier, ProjectVersion, DataItem } from "@/types";
import { deleteProjectVersion, getProjectVersions } from "@/api";
import { logModule, projectModule } from "@/store";
import { GenericSelector } from "@/components/common";
import { versionSelectorHeader } from "./headers";
import VersionCreator from "./VersionCreator.vue";
import ConfirmVersionDelete from "./ConfirmVersionDelete.vue";

/**
 * Displays list of project versions available to given project and allows them
 * to select, edit, delete, or create projects. Versions list is refreshed
 * whenever mounted or isOpen is changed to true.
 *
 * @emits-1 `selected` (ProjectVersion) - On version selected.
 * @emits-1 `unselected` - On version unselected.
 */
export default Vue.extend({
  components: { GenericSelector, VersionCreator, ConfirmVersionDelete },
  props: {
    /**
     * Whether this component is currently in view. If within
     * a stepper then this is true when the this component is within the current step.
     */
    isOpen: {
      type: Boolean,
      required: true,
    },
    /**
     * The currently selected project whose versions we are displaying.
     */
    project: {
      type: Object as PropType<ProjectIdentifier>,
      required: false,
    },
    hideCurrentVersion: {
      type: Boolean,
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
    this.loadProjectVersions();
  },
  watch: {
    project() {
      this.loadProjectVersions();
    },
  },
  computed: {
    loadedProjectVersionId(): string | undefined {
      return projectModule.versionId;
    },
    displayedVersions(): ProjectVersion[] {
      return this.hideCurrentVersion
        ? this.versions.filter(
            ({ versionId }) => versionId !== this.loadedProjectVersionId
          )
        : this.versions;
    },
  },
  methods: {
    onCreatorClose() {
      this.addVersionDialogue = false;
    },
    onSelectVersion(item: DataItem<ProjectVersion>) {
      if (item.value) {
        this.$emit("selected", item.item);
      } else {
        this.$emit("unselected");
      }
    },
    onAddItem() {
      this.addVersionDialogue = true;
    },
    onDeleteVersion(version: ProjectVersion) {
      this.versionToDelete = version;
      this.deleteVersionDialogue = true;
    },
    onVersionCreated(version: ProjectVersion) {
      this.versions = [version].concat(this.versions);
      this.addVersionDialogue = false;
      this.$emit("selected", version);
    },
    onCancelDeleteVersion() {
      this.deleteVersionDialogue = false;
    },
    onConfirmDeleteVersion(version: ProjectVersion) {
      this.deleteVersionDialogue = false;
      this.isLoading = true;
      deleteProjectVersion(version.versionId)
        .then(() => {
          logModule.onSuccess("Project version successfully deleted");
          this.versions = this.versions.filter(
            (v) => v.versionId != version.versionId
          );
        })
        .finally(() => (this.isLoading = false));
    },
    loadProjectVersions() {
      if (!this.project) return;

      this.isLoading = true;

      getProjectVersions(this.project.projectId)
        .then((versions: ProjectVersion[]) => {
          this.versions = versions;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
});
</script>
