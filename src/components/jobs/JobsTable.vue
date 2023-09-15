<template>
  <panel-card>
    <data-table
      :columns="jobColumns"
      :rows="rows"
      row-key="id"
      :loading="loading"
      :rows-per-page="10"
      :expanded="expanded"
      data-cy="job-table"
    >
      <template #body="quasarProps: { row: JobSchema; expand: boolean }">
        <job-row
          v-model:expanded="quasarProps.expand"
          :quasar-props="quasarProps"
          :job="quasarProps.row"
          @view-logs="jobApiStore.handleViewLogs"
        />
      </template>
    </data-table>

    <modal
      size="xl"
      title="Logs"
      :open="jobApiStore.jobLog.length > 0"
      @close="jobApiStore.handleCloseLogs"
    >
      <q-timeline data-cy="text-job-log">
        <q-virtual-scroll
          v-slot="{ item, index }: { item: JobLogStepSchema }"
          style="max-height: 70vh"
          :items="jobApiStore.jobLog"
          separator
        >
          <q-timeline-entry
            v-if="!!item.entry"
            :key="index"
            :subtitle="item.timestamp"
            :color="item.error ? 'negative' : 'positive'"
          >
            <q-expansion-item
              default-opened
              switch-toggle-side
              :label="item.stepName"
              class="text-h5"
            >
              <typography
                variant="expandable"
                l="3"
                :value="item.entry"
                default-expanded
                :collapse-length="0"
              />
            </q-expansion-item>
          </q-timeline-entry>
        </q-virtual-scroll>
      </q-timeline>
      <template #actions>
        <text-button
          label="Download Logs"
          icon="download"
          @click="jobApiStore.handleDownloadLogs"
        />
        <text-button
          color="negative"
          text
          icon="logs"
          label="Report a Bug"
          @click="handleFeedback"
        />
      </template>
    </modal>
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays a table of project job uploads.
 */
export default {
  name: "JobsTable",
};
</script>

<script setup lang="ts">
import { computed, onMounted } from "vue";
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { JobLogStepSchema, JobSchema } from "@/types";
import { FEEDBACK_LINK, jobColumns } from "@/util";
import { appStore, jobApiStore, jobStore } from "@/hooks";
import { DataTable, PanelCard, Modal, Typography } from "@/components/common";
import TextButton from "@/components/common/button/TextButton.vue";
import JobRow from "./JobRow.vue";

const rows = computed(() => jobStore.jobs);
const loading = computed(() => appStore.isLoading > 0);
const expanded = computed(() =>
  jobStore.selectedJob ? [jobStore.selectedJob.id] : []
);

/**
 * Routes the user to the feedback page.
 */
function handleFeedback(): void {
  window.open(FEEDBACK_LINK);
}

onMounted(() => jobApiStore.handleReload());
</script>
