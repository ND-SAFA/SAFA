<template>
  <panel-card>
    <data-table
      :columns="jobColumns"
      :expanded="expanded"
      :loading="loading"
      :rows="rows"
      :rows-per-page="10"
      data-cy="job-table"
      row-key="id"
    >
      <template #body="quasarProps: { row: JobSchema; expand: boolean }">
        <job-row
          v-model:expanded="quasarProps.expand"
          :job="quasarProps.row"
          :quasar-props="quasarProps"
          @view-logs="jobApiStore.handleViewLogs"
        />
      </template>
    </data-table>
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

<script lang="ts" setup>
import { computed, onMounted } from "vue";
import { JobSchema, JobTableProps } from "@/types";
import { jobColumns } from "@/util";
import { appStore, jobApiStore, jobStore } from "@/hooks";
import { DataTable, PanelCard } from "@/components/common";
import JobRow from "./JobRow.vue";

const props = defineProps<JobTableProps>();

const rows = computed(() =>
  props.displayProjectJobs ? jobStore.projectJobs : jobStore.jobs
);
const loading = computed(() => appStore.isLoading > 0);
const expanded = computed(() =>
  jobStore.selectedJob ? [jobStore.selectedJob.id] : []
);

onMounted(() => jobApiStore.handleReload());
</script>
