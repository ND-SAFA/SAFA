<template>
  <panel-card title="Data Integrations" :subtitle="subtitle">
    <template #title-actions>
      <text-button
        v-if="addOpen"
        text
        icon="cancel"
        label="Cancel import"
        @click="addOpen = false"
      />
    </template>

    <selector-table
      v-if="!addOpen"
      addable
      :columns="installationsColumns"
      :rows="rows"
      row-key="installationId"
      @row:add="addOpen = true"
    >
      <template #cell-actions="{ row }">
        <text-button
          text
          label="Re-Sync Data"
          color="primary"
          icon="sync"
          @click="handleSync(row)"
        />
      </template>
    </selector-table>

    <integrations-stepper v-else type="connect" @submit="addOpen = false" />
  </panel-card>
</template>

<script lang="ts">
/**
 * Renders a table of all active installations for the current project.
 */
export default {
  name: "ProjectInstallationsTable",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { InstallationSchema } from "@/types";
import { installationsColumns } from "@/util";
import { integrationsApiStore } from "@/hooks";
import { TextButton, SelectorTable, PanelCard } from "@/components/common";
import IntegrationsStepper from "./IntegrationsStepper.vue";

const addOpen = ref(false);

const rows = computed(() => integrationsApiStore.installations);

const subtitle = computed(() =>
  addOpen.value
    ? "Configure a new integration source."
    : "View data integration sources and synchronize data between them."
);

/**
 * Syncs the current project with the selected installation's data.
 * @param installation - THe installation to sync.
 */
function handleSync(installation: InstallationSchema): void {
  integrationsApiStore.handleSync(installation);
}
</script>
