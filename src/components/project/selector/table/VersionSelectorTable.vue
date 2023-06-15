<template>
  <selector-table
    v-model:selected="selectedItems"
    :minimal="props.minimal"
    addable
    :deletable="deletable"
    :loading="getVersionApiStore.getLoading"
    :columns="columns"
    :rows="rows"
    row-key="projectId"
    item-name="Project"
    data-cy="table-version"
    @refresh="handleReload"
    @row:add="handleOpenAdd"
    @row:delete="handleOpenDelete"
  >
    <template #bottom>
      <version-creator
        :open="addOpen"
        :project="props.project"
        @close="addOpen = false"
        @create="handleConfirmAdd"
      />
    </template>
  </selector-table>
</template>

<script lang="ts">
/**
 * A table for selecting project versions.
 */
export default {
  name: "VersionSelectorTable",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { IdentifierSchema, VersionSchema } from "@/types";
import { actionsColumn, versionColumns } from "@/util";
import {
  editProjectApiStore,
  getVersionApiStore,
  projectStore,
  sessionStore,
} from "@/hooks";
import { SelectorTable } from "@/components/common";
import { VersionCreator } from "@/components/project/creator";

const props = defineProps<{
  /**
   * The project to select a version from.
   */
  project: IdentifierSchema;
  /**
   * Whether this component is currently in view.
   * The content will be reloaded when opened.
   */
  open: boolean;
  /**
   * Whether to display minimal information.
   */
  minimal?: boolean;
  /**
   * If true, the current version will be hidden.
   */
  hideCurrentVersion?: boolean;
}>();

const emit = defineEmits<{
  /**
   * Emitted when the selected version changes.
   */
  (e: "selected", version: VersionSchema | undefined): void;
}>();

const selected = ref<VersionSchema | undefined>();
const addOpen = ref(false);
const versions = ref<VersionSchema[]>([]);

const selectedItems = computed({
  get() {
    return selected.value ? [selected.value] : [];
  },
  set(items: VersionSchema[]) {
    selected.value = items[0];
    emit("selected", items[0]);
  },
});

const columns = computed(() =>
  props.minimal ? versionColumns : [...versionColumns, actionsColumn]
);

const rows = computed(() =>
  props.hideCurrentVersion
    ? versions.value.filter(
        ({ versionId }) => versionId !== projectStore.versionId
      )
    : versions.value
);

const deletable = computed(
  () => sessionStore.isEditor(props.project) && versions.value.length > 1
);

/**
 * Loads project versions.
 */
function handleReload() {
  getVersionApiStore.handleGetProjectVersions(props.project.projectId, {
    onSuccess: (loadedVersions) => (versions.value = loadedVersions),
  });
}

/**
 * Opens the add version modal.
 */
function handleOpenAdd() {
  addOpen.value = true;
}

/**
 * Closes the add version modal and adds the created version.
 */
function handleConfirmAdd(version: VersionSchema) {
  versions.value = [version, ...versions.value];
  addOpen.value = false;
}

/**
 * Attempts to delete the version.
 * @param version - The version to delete.
 */
function handleOpenDelete(version: VersionSchema) {
  editProjectApiStore.handleDeleteVersion(version, {
    onSuccess: () => {
      versions.value = versions.value.filter(
        ({ versionId }) => versionId != version.versionId
      );
    },
  });
}

onMounted(() => handleReload());

watch(
  () => props.project,
  () => handleReload()
);

watch(
  () => props.open,
  () => handleReload()
);
</script>
