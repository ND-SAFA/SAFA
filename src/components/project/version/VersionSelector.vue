<template>
  <generic-selector
    v-if="this.isOpen"
    item-key="versionId"
    no-data-text="Project contains no versions"
    :headers="headers"
    :items="displayedVersions"
    :is-open="isOpen"
    :is-loading="isLoading"
    :minimal="minimal"
    :has-edit="false"
    :has-add="showEdit"
    :has-delete="showEdit"
    :can-delete-last-item="false"
    data-cy="table-version"
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
import { IdentifierModel, VersionModel, DataItem, ProjectRole } from "@/types";
import { projectStore, sessionStore } from "@/hooks";
import { getProjectVersions, handleDeleteVersion } from "@/api";
import { GenericSelector } from "@/components/common";
import ConfirmVersionDelete from "./ConfirmVersionDelete.vue";
import VersionCreator from "./VersionCreator.vue";

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
      type: Object as PropType<IdentifierModel>,
      required: false,
    },
    hideCurrentVersion: {
      type: Boolean,
      required: false,
    },
    minimal: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    const baseHeaders = [
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
    ];

    return {
      headers: this.minimal
        ? baseHeaders
        : [
            ...baseHeaders,
            { text: "Actions", value: "actions", sortable: false },
          ],
      versions: [] as VersionModel[],
      versionToDelete: undefined as VersionModel | undefined,
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
    displayedVersions(): VersionModel[] {
      return this.hideCurrentVersion
        ? this.versions.filter(
            ({ versionId }) => versionId !== projectStore.versionId
          )
        : this.versions;
    },
    /**
     * @return Whether to allow this user to add or delete a version.
     */
    showEdit(): boolean {
      return sessionStore.isEditor(this.project);
    },
  },
  methods: {
    /**
     * Loads project versions.
     */
    handleLoadProjectVersions() {
      if (!this.project?.projectId) return;

      this.isLoading = true;

      getProjectVersions(this.project.projectId)
        .then((versions: VersionModel[]) => {
          this.versions = versions;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    /**
     * Emits selected versions.
     */
    handleSelectVersion(item: DataItem<VersionModel>) {
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
    handleVersionCreated(version: VersionModel) {
      this.versions = [version, ...this.versions];
      this.addVersionDialogue = false;
      this.$emit("selected", version);
    },
    /**
     * Opens the version deletion modal.
     * @param version - The version to delete.
     */
    handleDeleteVersion(version: VersionModel) {
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
    handleConfirmDeleteVersion(version: VersionModel) {
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
