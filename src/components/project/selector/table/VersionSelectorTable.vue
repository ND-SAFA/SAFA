<template>
  <selector-table
    v-model:selected="selectedItems"
    :minimal="props.minimal"
    :addable="addable"
    :deletable="deletable"
    :loading="getVersionApiStore.getLoading"
    :columns="columns"
    :rows="rows"
    :disabled="props.disabled ? true : undefined"
    row-key="projectId"
    item-name="version"
    :icons="{ add: 'version-add', edit: 'edit', delete: 'version-delete' }"
    data-cy="table-version"
    @refresh="handleReload"
    @row:add="addOpen = true"
    @row:delete="handleDelete"
  >
    <template #bottom>
      <create-version-modal
        :open="addOpen"
        :project="props.project"
        @close="addOpen = false"
        @create="handleAdd"
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
import { VersionSchema, VersionSelectorTableProps } from "@/types";
import { actionsColumn, versionColumns } from "@/util";
import { getVersionApiStore, projectStore, permissionStore } from "@/hooks";
import { SelectorTable } from "@/components/common";
import { CreateVersionModal } from "@/components/project/creator";

const props = defineProps<VersionSelectorTableProps>();

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

const addable = computed(() =>
  permissionStore.isAllowed("project.edit_versions", props.project)
);
const deletable = computed(() => addable.value && versions.value.length > 1);

/**
 * Loads project versions.
 */
function handleReload() {
  getVersionApiStore.handleLoadVersions(props.project.projectId, {
    onSuccess: (loadedVersions) => {
      versions.value = loadedVersions;

      if (loadedVersions.length === 1 && props.minimal) {
        emit("selected", loadedVersions[0]);
      }
    },
  });
}

/**
 * Closes the add version modal and adds the created version.
 */
function handleAdd(version: VersionSchema) {
  versions.value = [version, ...versions.value];
  addOpen.value = false;
}

/**
 * Attempts to delete the version.
 * @param version - The version to delete.
 */
function handleDelete(version: VersionSchema) {
  getVersionApiStore.handleDelete(version, {
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
