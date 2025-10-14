<template>
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
        icon="graph-refresh"
        label="Reload Logs"
        @click="jobApiStore.handleViewLogs(jobStore.selectedJob!)"
      />
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
</template>

<script lang="ts">
/**
 * Displays a modal with logs for the currently selected job.
 */
export default {
  name: "JobLogModal",
};
</script>

<script lang="ts" setup>
import { JobLogStepSchema } from "@/types";
import { FEEDBACK_LINK } from "@/util";
import { jobApiStore, jobStore } from "@/hooks";
import { TextButton, Modal, Typography } from "@/components/common";

/**
 * Routes the user to the feedback page.
 */
function handleFeedback(): void {
  window.open(FEEDBACK_LINK);
}
</script>
