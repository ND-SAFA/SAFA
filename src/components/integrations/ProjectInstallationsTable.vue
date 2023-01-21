<template>
  <panel-card>
    <typography el="h2" variant="subtitle" value="Data Integrations" />
    <v-data-table
      :headers="headers"
      :items="installations"
      :loading="isLoading"
      item-key="installationId"
      class="mt-5"
    >
      <template v-slot:[`item.lastUpdate`]="{ item }">
        <span>
          {{ getDateDisplay(item.lastUpdate) }}
        </span>
      </template>

      <template v-slot:[`item.actions`]="{ item }">
        <text-button
          text
          color="primary"
          icon-id="mdi-cached"
          @click="handleSync(item)"
        >
          Re-Sync Data
        </text-button>
      </template>

      <template v-slot:[`footer.prepend`]>
        <div class="py-3">
          <icon-button
            fab
            color="primary"
            icon-id="mdi-plus"
            tooltip="Import New Project"
            data-cy="button-integration-add"
            @click="modalOpen = true"
          />
          <modal
            :is-open="modalOpen"
            title="Import Data"
            :actions-height="0"
            @close="modalOpen = false"
          >
            <template v-slot:body>
              <integrations-stepper
                type="connect"
                @submit="modalOpen = false"
              />
            </template>
          </modal>
        </div>
      </template>
    </v-data-table>
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { InstallationSchema } from "@/types";
import { timestampToDisplay } from "@/util";
import { integrationsStore } from "@/hooks";
import { handleSyncInstallation } from "@/api";
import {
  Typography,
  IconButton,
  Modal,
  PanelCard,
  TextButton,
} from "@/components/common";
import IntegrationsStepper from "./IntegrationsStepper.vue";

/**
 * Renders a table of all active installations for the current project.
 */
export default Vue.extend({
  name: "ProjectInstallationsTable",
  components: {
    TextButton,
    PanelCard,
    IntegrationsStepper,
    Modal,
    Typography,
    IconButton,
  },
  data() {
    return {
      modalOpen: false,
      isLoading: false,
      headers: [
        { text: "Integration Type", value: "type" },
        { text: "Project ID", value: "installationId" },
        { text: "Last Synced", value: "lastUpdate" },
        { text: "Actions", value: "actions", sortable: false },
      ],
    };
  },
  computed: {
    /**
     * @return All project installations.
     */
    installations(): InstallationSchema[] {
      return integrationsStore.installations;
    },
  },
  methods: {
    /**
     * @returns The display name for when this installation was last synced.
     */
    getDateDisplay(timestamp: string) {
      return timestampToDisplay(timestamp);
    },
    /**
     * Syncs the current project with the selected installation's data.
     * @param installation - THe installation to sync.
     */
    handleSync(installation: InstallationSchema): void {
      this.isLoading = true;

      handleSyncInstallation(installation, {
        onComplete: () => (this.isLoading = false),
      });
    },
  },
});
</script>
