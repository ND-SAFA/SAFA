<template>
  <panel-card>
    <data-table
      :columns="jobColumns"
      :rows="rows"
      row-key="id"
      :loading="loading"
      :rows-per-page="10"
      :expanded="expanded"
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

    <modal title="Logs" :open="jobLog.length > 0" @close="handleCloseLogs">
      <typography
        t="4"
        default-expanded
        variant="code"
        :value="logText"
        data-cy="text-job-log"
      />
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
import { jobColumns } from "@/util";
import { appStore, jobStore } from "@/hooks";
import { getJobLog, handleReloadJobs } from "@/api";
import { DataTable, PanelCard, Modal, Typography } from "@/components/common";
import JobRow from "./JobRow.vue";

const jobLog = ref<JobLogSchema[]>([]);

const rows = computed(() => jobStore.jobs);
const loading = computed(() => appStore.isLoading > 0);
const logText = computed(() => JSON.stringify(jobLog.value, null, 2));
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
}

/**
 * Closes the job log.
 */
function handleCloseLogs(): void {
  jobLog.value = [];
}

onMounted(() => handleReload());
</script>
