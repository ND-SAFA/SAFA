<template>
  <panel-card :title="panelTitle">
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

    <modal
      :open="jobApiStore.jobLog.length > 0"
      size="xl"
      title="Logs"
      @close="jobApiStore.handleCloseLogs"
    >
      <q-timeline data-cy="text-job-log">
        <q-virtual-scroll
          v-slot="{ item, index }: { item: JobLogStepSchema; index: number }"
          :items="jobApiStore.jobLog"
          separator
          style="max-height: 70vh"
        >
          <q-timeline-entry
            v-if="!!item.entry"
            :key="index"
            :color="item.error ? 'negative' : 'positive'"
            :subtitle="item.timestamp"
          >
            <q-expansion-item
              :label="item.stepName"
              class="text-h5"
              default-opened
              switch-toggle-side
            >
              <typography
                :collapse-length="0"
                :value="item.entry"
                default-expanded
                l="3"
                variant="expandable"
              />
            </q-expansion-item>
          </q-timeline-entry>
        </q-virtual-scroll>
      </q-timeline>
      <template #actions>
        <text-button
          text
          icon="download"
          label="Download Logs"
          @click="jobApiStore.handleDownloadLogs"
        />
        <text-button
          color="negative"
          icon="logs"
          label="Report a Bug"
          text
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

<script lang="ts" setup>
import { computed, onMounted } from "vue";
import { JobLogStepSchema, JobSchema, JobTableProps } from "@/types";
import { FEEDBACK_LINK, jobColumns } from "@/util";
import { appStore, jobApiStore, jobStore } from "@/hooks";
import { DataTable, PanelCard, Modal, Typography } from "@/components/common";
import TextButton from "@/components/common/button/TextButton.vue";
import JobRow from "./JobRow.vue";

const props = defineProps<JobTableProps>();

const panelTitle = computed(() =>
  props.displayProjectJobs ? "Project Tasks" : "Recent Tasks"
);
const rows = computed(() =>
  props.displayProjectJobs ? jobStore.projectJobs : jobStore.jobs
);
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
