<template>
  <selector-table
    v-model:selected="selectedItems"
    :minimal="props.minimal"
    addable
    editable
    :deletable="isDeletable"
    :loading="loading"
    :columns="columns"
    :rows="rows"
    row-key="projectId"
    item-name="Project"
    @refresh="handleReload"
    @row:add="handleOpenAdd"
    @row:edit="handleOpenEdit"
    @row:delete="handleOpenDelete"
  >
    <template #bottom>
      <confirm-project-delete
        :open="deleteOpen"
        @close="deleteOpen = false"
        @confirm="handleConfirmDelete"
      />
      <project-identifier-modal
        :open="saveOpen"
        @close="saveOpen = false"
        @save="handleConfirmSave"
      />
    </template>
  </selector-table>
</template>

<script lang="ts">
/**
 * A table for selecting projects.
 */
export default {
  name: "ProjectSelectorTable",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { IdentifierSchema } from "@/types";
import { projectExpandedColumns, projectNameColumn } from "@/util";
import { identifierSaveStore, projectStore, sessionStore } from "@/hooks";
import { handleGetProjects } from "@/api";
import { SelectorTable } from "@/components/common";
import { ConfirmProjectDelete, ProjectIdentifierModal } from "../base";

const props = defineProps<{
  /**
   * Whether this component is currently in view.
   * The content will be reloaded when opened.
   */
  open: boolean;
  /**
   * Whether to display minimal information.
   */
  minimal?: boolean;
}>();

const emit = defineEmits<{
  /**
   * Emitted when the selected project changes.
   */
  (e: "selected", project: IdentifierSchema | undefined): void;
}>();

const currentRoute = useRoute();

const selected = ref<IdentifierSchema | undefined>();
const loading = ref(true);
const saveOpen = ref(false);
const deleteOpen = ref(false);

const selectedItems = computed({
  get() {
    return selected.value ? [selected.value] : [];
  },
  set(items: IdentifierSchema[]) {
    selected.value = items[0];
    emit("selected", items[0]);
  },
});

const columns = computed(() =>
  props.minimal
    ? [projectNameColumn]
    : [projectNameColumn, ...projectExpandedColumns]
);

const rows = computed(() => projectStore.allProjects);

/**
 * Loads all projects.
 */
function handleReload() {
  loading.value = true;

  handleGetProjects({
    onComplete: () => (loading.value = false),
  });
}

/**
 * Returns whether a project is deletable.
 * @param project - The project to check.
 * @return Whether it can be deleted.
 */
function isDeletable(project: IdentifierSchema): boolean {
  return sessionStore.isOwner(project);
}

/**
 * Opens the add project modal.
 */
function handleOpenAdd() {
  identifierSaveStore.baseIdentifier = undefined;
  saveOpen.value = true;
}

/**
 * Opens the edit project modal.
 * @param project - The project to edit.
 */
function handleOpenEdit(project: IdentifierSchema) {
  identifierSaveStore.baseIdentifier = project;
  saveOpen.value = true;
}

/**
 * Opens the delete project modal.
 * @param project - The project to delete.
 */
function handleOpenDelete(project: IdentifierSchema) {
  identifierSaveStore.baseIdentifier = project;
  deleteOpen.value = true;
}

/**
 * Closes the delete project modal.
 */
function handleConfirmDelete() {
  deleteOpen.value = false;
  selectedItems.value = [];
}

/**
 * Closes the save project modal.
 */
function handleConfirmSave() {
  saveOpen.value = false;
}

/**
 * Loads all projects when opened.
 */
watch(
  () => props.open,
  (open) => {
    if (!open) return;

    handleReload();
  }
);

/**
 * Loads all projects when the page changes.
 */
watch(
  () => currentRoute.path,
  () => handleReload()
);

/**
 * Loads all projects when mounted.
 */
onMounted(() => handleReload());
</script>
