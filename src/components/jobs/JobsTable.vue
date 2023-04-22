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
      <template #body="quasarProps">
        <job-row
          v-model:expanded="quasarProps.expand"
          :quasar-props="quasarProps"
          :job="quasarProps.row"
          @view-logs="handleViewLogs"
        />
      </template>
    </data-table>

    <modal
      size="xl"
      title="Logs"
      :open="jobLog.length > 0"
      @close="handleCloseLogs"
    >
      <q-timeline data-cy="text-job-log">
        <template v-for="(items, idx) in jobLog" :key="idx">
          <q-timeline-entry
            v-for="item in items"
            :key="item.entry"
            :subtitle="timestampToDisplay(item.timestamp)"
            :title="jobSteps[idx]"
          >
            <typography
              v-for="line in item.entry.split('\n')"
              :key="line"
              el="p"
              :value="line"
            />
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
import { computed, onMounted, ref } from "vue";
import { JobLogSchema, JobSchema } from "@/types";
import { jobColumns, timestampToDisplay } from "@/util";
import { appStore, jobStore } from "@/hooks";
import { getJobLog, handleReloadJobs } from "@/api";
import { DataTable, PanelCard, Modal, Typography } from "@/components/common";
import JobRow from "./JobRow.vue";

const jobLog = ref<JobLogSchema[][]>([]);
const jobSteps = ref<string[]>([]);

const rows = computed(() => jobStore.jobs);
const loading = computed(() => appStore.isLoading > 0);
const expanded = computed(() =>
  jobStore.selectedJob ? [jobStore.selectedJob.id] : []
);

/**
 * Reloads the list of jobs.
 */
function handleReload() {
  handleReloadJobs();
}

/**
 * Gets the log for a job.
 * @param job - The job to view.
 */
async function handleViewLogs(job: JobSchema): Promise<void> {
  jobLog.value = await getJobLog(job.id);
  jobSteps.value = job.steps;
}

/**
 * Closes the job log.
 */
function handleCloseLogs(): void {
  jobLog.value = [];
  jobSteps.value = [];
}

onMounted(() => handleReload());
</script>
