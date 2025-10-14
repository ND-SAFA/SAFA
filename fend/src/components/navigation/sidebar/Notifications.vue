<template>
  <list-item
    to=""
    title="Notifications"
    clickable
    tooltip="Notifications"
    @click="handleOpen"
  >
    <template #icon>
      <div class="nav-job-icon">
        <q-circular-progress
          v-if="displayInProgressJobs"
          :color="color"
          indeterminate
          size="md"
        />
      </div>
      <div>
        <icon variant="notification" size="sm" color="text" />
        <q-badge
          v-if="displayUpdates"
          :color="color"
          rounded
          floating
          :label="updates"
          class="nav-job-badge"
        />
      </div>

      <q-menu v-model="open">
        <list v-if="displayRecentJobs" class="nav-notifications q-pa-sm">
          <typography variant="caption" value="Jobs" />

          <list-item
            v-for="job in recentJobs"
            :key="job.id"
            dense
            clickable
            :title="job.name"
            :subtitle="job.steps[job.currentStep]"
            @click="handleClickJob(job)"
          >
            <template #icon>
              <q-circular-progress
                v-if="job.status === 'IN_PROGRESS'"
                color="secondary"
                :value="job.currentProgress"
                size="sm"
              />
              <icon
                v-else-if="job.status === 'COMPLETED'"
                variant="job-complete"
                color="primary"
              />
              <icon
                v-else-if="job.status === 'FAILED'"
                variant="job-fail"
                color="error"
              />
            </template>
          </list-item>
        </list>

        <list
          v-if="notifications.length > 0"
          class="nav-notifications q-pa-sm q-mb-sm"
        >
          <typography variant="caption" value="Notifications" />

          <list-item
            v-for="item in notifications"
            :key="item.message"
            dense
            :title="item.message"
          >
            <template #icon>
              <icon
                v-if="item.type === 'success'"
                variant="save"
                color="added"
              />
              <icon
                v-if="item.type === 'error'"
                variant="error"
                color="removed"
              />
              <icon
                v-if="item.type === 'warning'"
                variant="warning"
                color="warning"
              />
              <icon
                v-if="item.type === 'info'"
                variant="logs"
                color="modified"
              />
            </template>
          </list-item>
        </list>

        <div
          v-if="notifications.length === 0 && !displayRecentJobs"
          class="q-pa-md"
        >
          <typography
            value="There are no notifications in the current session."
          />
        </div>
      </q-menu>
    </template>
  </list-item>
</template>

<script lang="ts">
/**
 * Displays the user's notifications.
 */
export default {
  name: "Notifications",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { JobSchema } from "@/types";
import { getVersionApiStore, jobStore, logStore } from "@/hooks";
import { navigateTo, Routes } from "@/router";
import { Typography, Icon, List, ListItem } from "@/components/common";

const viewedMessages = ref(0);
const open = ref(false);

const notifications = computed(() => logStore.notifications);
const newNotifications = computed(() =>
  Math.max(notifications.value.length - viewedMessages.value, 0)
);

const inProgressJobs = computed(() => jobStore.inProgressJobs);
const recentJobs = computed(() => jobStore.recentJobs);
const displayInProgressJobs = computed(() => inProgressJobs.value.length > 0);
const displayRecentJobs = computed(() => recentJobs.value.length > 0);

const displayUpdates = computed(
  () => newNotifications.value > 0 || inProgressJobs.value.length > 0
);
const updates = computed(
  () => newNotifications.value + inProgressJobs.value.length
);

const color = computed(() => (inProgressJobs.value ? "primary" : "secondary"));

/**
 * Sets all messages to viewed on open.
 */
function handleOpen() {
  open.value = true;
  viewedMessages.value = notifications.value.length;
}

/**
 * WHen a job is clicked, open the project if the job is completed, or open the upload status page.
 * @param job - The job to open.
 */
function handleClickJob(job: JobSchema) {
  if (job.completedEntityId) {
    getVersionApiStore.handleLoad(job.completedEntityId);
  } else {
    navigateTo(Routes.UPLOAD_STATUS);
  }
}
</script>
