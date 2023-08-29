<template>
  <panel-card title="Teams" :subtitle="subtitle">
    <template #title-actions>
      <text-button
        v-if="addMode"
        text
        label="Cancel"
        icon="cancel"
        @click="handleClose"
      />
    </template>

    <data-table
      v-if="!addMode"
      :expanded="expanded"
      :columns="teamColumns"
      :rows="rows"
      :loading="loading"
      row-key="id"
    >
      <template #body="quasarProps">
        <q-tr :props="quasarProps">
          <q-td class="data-table-cell-300">
            <icon-button
              tooltip="Toggle expand"
              :icon="expanded.includes(quasarProps.row.id) ? 'down' : 'up'"
              class="q-mr-md"
              @click="handleToggleExpand(quasarProps as any)"
            />
            <typography :value="quasarProps.row.name" />
          </q-td>
          <q-td align="end">
            <typography :value="quasarProps.row.members.length" />
          </q-td>
          <q-td align="end">
            <typography :value="quasarProps.row.projects.length" />
          </q-td>
          <q-td align="end"> </q-td>
        </q-tr>
        <q-tr
          v-show="expanded.includes(quasarProps.row.id)"
          :props="quasarProps"
        >
          <q-td colspan="100%"></q-td>
        </q-tr>
      </template>
    </data-table>
  </panel-card>
</template>

<script lang="ts">
/**
 * A tab for managing teams within an organization.
 */
export default {
  name: "TeamTab",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { teamColumns } from "@/util";
import {
  PanelCard,
  TextButton,
  DataTable,
  IconButton,
  Typography,
} from "@/components/common";

const loading = ref(false);
const addMode = ref(false);
const expanded = ref<string[]>([]);

const subtitle = computed(() =>
  addMode.value ? "Create a new team." : "Manage teams and permissions."
);

const rows = [
  {
    id: "1",
    name: "Team 1",
    members: "12345",
    projects: "123",
  },
  {
    id: "2",
    name: "Team 2",
    members: "123",
    projects: "1",
  },
];

/**
 * Closes the add team form and resets entered data.
 */
function handleClose() {
  addMode.value = false;
}

/**
 * Toggles the expanded state of a row.
 * @param quasarProps - The row to toggle.
 */
function handleToggleExpand(quasarProps: {
  row: { id: string };
  expand: boolean;
}): void {
  const { id } = quasarProps.row;
  const idx = expanded.value.indexOf(id);

  if (idx === -1) {
    expanded.value.push(id);
  } else {
    expanded.value.splice(idx, 1);
  }

  quasarProps.expand = !quasarProps.expand;
}
</script>
