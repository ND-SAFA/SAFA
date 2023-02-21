<template>
  <selector-table
    v-model:selected="selectedItems"
    :loading="loading"
    :columns="columns"
    :rows="rows"
    row-key="projectId"
  >
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
import { IdentifierSchema, TableColumn } from "@/types";
import { projectStore } from "@/hooks";
import { handleGetProjects } from "@/api";
import { SelectorTable } from "@/components/common";

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
const loading = ref(false);

const selectedItems = computed({
  get() {
    return selected.value ? [selected.value] : [];
  },
  set(items: IdentifierSchema[]) {
    selected.value = items[0];
    emit("selected", items[0]);
  },
});

const nameColumn: TableColumn<IdentifierSchema> = {
  name: "name",
  label: "Name",
  sortable: true,
  field: (row) => row.name,
};

const expandedColumns: TableColumn<IdentifierSchema>[] = [
  {
    name: "description",
    label: "Description",
    sortable: false,
    field: (row) => row.description,
  },
  {
    name: "owner",
    label: "Owner",
    sortable: false,
    field: (row) => row.owner,
  },
  {
    name: "actions",
    label: "Actions",
    sortable: false,
    field: () => "",
  },
];

const columns = computed(() =>
  props.minimal ? [nameColumn] : [nameColumn, ...expandedColumns]
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
