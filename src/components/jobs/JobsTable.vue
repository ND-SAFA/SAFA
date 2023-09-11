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
      <template #body="quasarProps: { row: JobSchema, expand: boolean }">
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
        <template v-for="(items, idx) in jobApiStore.jobLog" :key="idx">
          <q-timeline-entry
            v-for="item in items"
            :key="item.entry"
            :subtitle="timestampToDisplay(item.timestamp)"
          >
            <q-expansion-item
              default-opened
              switch-toggle-side
              :label="jobApiStore.jobSteps[idx]"
              class="text-h5"
            >
              <typography
                v-for="line in item.entry.split('\n')"
                :key="line"
                el="p"
                l="3"
                :value="line"
              />
            </q-expansion-item>
          </q-timeline-entry>
        </template>
      </q-timeline>
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
import { JobSchema } from "@/types";
import { jobColumns, timestampToDisplay } from "@/util";
import { appStore, jobApiStore, jobStore } from "@/hooks";
import { DataTable, PanelCard, Modal, Typography } from "@/components/common";
import JobRow from "./JobRow.vue";

const rows = computed(() => jobStore.jobs);
const loading = computed(() => appStore.isLoading > 0);
const expanded = computed(() =>
  jobStore.selectedJob ? [jobStore.selectedJob.id] : []
);

onMounted(() => jobApiStore.handleReload());
</script>
