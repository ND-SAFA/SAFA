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
    @item:select="handleSelectVersion"
    @item:delete="handleDeleteVersion"
    @item:add="handleAddItem"
    @refresh="handleLoadProjectVersions"
  >
    <template v-slot:addItemDialogue>
      <version-creator
        :is-open="addVersionDialogue"
        :project="project"
        @close="handleCreatorClose"
        @create="handleVersionCreated"
      />
    </template>
    <template v-slot:deleteItemDialogue>
      <confirm-version-delete
        :version="versionToDelete"
        :delete-dialogue="deleteVersionDialogue"
        @cancel="handleCancelDeleteVersion"
        @confirm="handleConfirmDeleteVersion"
      />
    </template>
  </generic-selector>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ProjectIdentifier, ProjectVersion, DataItem } from "@/types";
import { getProjectVersions, handleDeleteVersion } from "@/api";
import { projectModule } from "@/store";
import { GenericSelector } from "@/components/common";
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
  name: "VersionSelector",
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
      headers: [
        {
          text: "Major",
          value: "majorVersion",
          sortable: true,
          isSelectable: true,
        },
        {
          text: "Minor",
          value: "minorVersion",
          sortable: true,
          isSelectable: true,
        },
        {
          text: "Revision",
          value: "revision",
          sortable: true,
          isSelectable: true,
        },
        { text: "Actions", value: "actions", sortable: false },
      ],
      versions: [] as ProjectVersion[],
      versionToDelete: undefined as ProjectVersion | undefined,
      deleteVersionDialogue: false,
      addVersionDialogue: false,
      isLoading: false,
    };
  },
  mounted() {
    this.handleLoadProjectVersions();
  },
  watch: {
    project() {
      this.handleLoadProjectVersions();
    },
  },
  computed: {
    /**
     * @return The displayed versions.
     */
    displayedVersions(): ProjectVersion[] {
      return this.hideCurrentVersion
        ? this.versions.filter(
            ({ versionId }) => versionId !== projectModule.versionId
          )
        : this.versions;
    },
  },
  methods: {
    /**
     * Loads project versions.
     */
    handleLoadProjectVersions() {
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
    /**
     * Emits selected versions.
     */
    handleSelectVersion(item: DataItem<ProjectVersion>) {
      if (item.value) {
        this.$emit("selected", item.item);
      } else {
        this.$emit("unselected");
      }
    },
    /**
     * Opens the version add modal.
     */
    handleAddItem() {
      this.addVersionDialogue = true;
    },
    /**
     * Closes the version add modal.
     */
    handleCreatorClose() {
      this.addVersionDialogue = false;
    },
    /**
     * Adds the new version the version list, and emits the new version to select.
     * @param version - The new version.
     */
    handleVersionCreated(version: ProjectVersion) {
      this.versions = [version, ...this.versions];
      this.addVersionDialogue = false;
      this.$emit("selected", version);
    },
    /**
     * Opens the version deletion modal.
     * @param version - The version to delete.
     */
    handleDeleteVersion(version: ProjectVersion) {
      this.versionToDelete = version;
      this.deleteVersionDialogue = true;
    },
    /**
     * Closes the version deletion modal.
     */
    handleCancelDeleteVersion() {
      this.deleteVersionDialogue = false;
    },
    /**
     * Attempts to delete the version.
     * @param version - The version to delete.
     */
    handleConfirmDeleteVersion(version: ProjectVersion) {
      this.deleteVersionDialogue = false;
      this.isLoading = true;

      handleDeleteVersion(version.versionId, {
        onSuccess: () => {
          this.isLoading = false;
          this.versions = this.versions.filter(
            (v) => v.versionId != version.versionId
          );
        },
        onError: () => (this.isLoading = false),
      });
    },
  },
});
</script>
