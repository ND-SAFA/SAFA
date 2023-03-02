<template>
  <panel-card
    title="Data Integrations"
    subtitle="View data integration sources and synchronize data between them."
  >
    <selector-table
      addable
      :columns="installationsColumns"
      :rows="rows"
      row-key="installationId"
      @row:add="modalOpen = true"
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
    <modal
      :open="modalOpen"
      size="lg"
      title="Import Data"
      @close="modalOpen = false"
    >
      <integrations-stepper type="connect" @submit="modalOpen = false" />
    </modal>
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
import { timestampToDisplay } from "@/util";
import { integrationsStore } from "@/hooks";
import { handleSyncInstallation } from "@/api";
import {
  Modal,
  TextButton,
  SelectorTable,
  PanelCard,
} from "@/components/common";
import IntegrationsStepper from "./IntegrationsStepper.vue";
import { installationsColumns } from "./headers";

const modalOpen = ref(false);
const loading = ref(false);

const rows = computed(() =>
  integrationsStore.installations.map((installation) => ({
    ...installation,
    lastUpdate: timestampToDisplay(installation.lastUpdate),
  }))
);

/**
 * Syncs the current project with the selected installation's data.
 * @param installation - THe installation to sync.
 */
function handleSync(installation: InstallationSchema): void {
  loading.value = true;

  handleSyncInstallation(installation, {
    onComplete: () => (loading.value = false),
  });
}
</script>
