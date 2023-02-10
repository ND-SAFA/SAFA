<template>
  <table-selector
    v-if="isOpen"
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
    class="version-table"
    @item:select="handleSelectVersion"
    @item:delete="handleDelete"
    @item:add="handleAddItem"
    @refresh="handleLoadProjectVersions"
  >
    <template #addItemDialogue>
      <version-creator
        :is-open="addVersionDialogue"
        :project="project"
        @close="handleCreatorClose"
        @create="handleVersionCreated"
      />
    </template>
  </table-selector>
</template>

<script lang="ts">
/**
 * Displays list of project versions available to given project and allows them
 * to select, edit, delete, or create projects. Versions list is refreshed
 * whenever mounted or isOpen is changed to true.
 */
export default {
  name: "VersionSelector",
};
</script>

<script setup lang="ts">
import { defineEmits, defineProps, onMounted, ref, computed, watch } from "vue";
import { IdentifierSchema, VersionSchema } from "@/types";
import { projectStore, sessionStore } from "@/hooks";
import { getProjectVersions, handleDeleteVersion } from "@/api";
import { TableSelector } from "@/components/common";
import VersionCreator from "./VersionCreator.vue";

const props = defineProps<{
  /**
   * Whether this component is currently in view. If within
   * a stepper then this is true when this component is within the current step.
   */
  isOpen: boolean;
  project?: IdentifierSchema;
  hideCurrentVersion?: boolean;
  minimal?: boolean;
}>();

const emit = defineEmits<{
  (e: "selected", version: VersionSchema): void;
  (e: "unselected"): void;
}>();

const versions = ref<VersionSchema[]>([]);
const addVersionDialogue = ref(false);
const isLoading = ref(false);

const headers = computed(() => {
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
  const actionsHeader = { text: "Actions", value: "actions", sortable: false };

  return props.minimal ? baseHeaders : [...baseHeaders, actionsHeader];
});

const displayedVersions = computed(() =>
  props.hideCurrentVersion
    ? versions.value.filter(
        ({ versionId }) => versionId !== projectStore.versionId
      )
    : versions.value
);

const showEdit = computed(
  () => props.project && sessionStore.isEditor(props.project)
);

/**
 * Loads project versions.
 */
function handleLoadProjectVersions() {
  if (!props.project?.projectId) return;

  isLoading.value = true;

  getProjectVersions(props.project.projectId)
    .then((loadedVersions: VersionSchema[]) => {
      versions.value = loadedVersions;
    })
    .finally(() => {
      isLoading.value = false;
    });
}

/**
 * Emits selected versions.
 */
function handleSelectVersion(item: VersionSchema) {
  if (item) {
    emit("selected", item);
  } else {
    emit("unselected");
  }
}

/**
 * Opens the version add modal.
 */
function handleAddItem() {
  addVersionDialogue.value = true;
}

/**
 * Closes the version add modal.
 */
function handleCreatorClose() {
  addVersionDialogue.value = false;
}

/**
 * Adds the new version the version list, and emits the new version to select.
 * @param version - The new version.
 */
function handleVersionCreated(version: VersionSchema) {
  versions.value = [version, ...versions.value];
  addVersionDialogue.value = false;
}

/**
 * Attempts to delete the version.
 * @param version - The version to delete.
 */
function handleDelete(version: VersionSchema) {
  handleDeleteVersion(version, {
    onSuccess: () => {
      versions.value = versions.value.filter(
        ({ versionId }) => versionId != version.versionId
      );
    },
  });
}

onMounted(() => handleLoadProjectVersions());

watch(
  () => props.project,
  () => handleLoadProjectVersions()
);
</script>
