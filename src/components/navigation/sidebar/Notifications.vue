<template>
  <div>
    <q-circular-progress
      v-if="displayInProgressJobs"
      :color="color"
      indeterminate
      size="md"
      class="nav-job-icon"
    />
    <q-btn round flat @click="handleClearNewMessages">
      <icon variant="notification" />
      <q-tooltip :delay="200">View notifications</q-tooltip>
      <q-badge v-if="displayUpdates" :color="color" floating rounded>
        {{ updates }}
      </q-badge>
      <q-menu>
        <list v-if="displayRecentJobs" class="nav-notifications q-pa-sm">
          <typography variant="caption" value="Jobs" />

          <list-item
            v-for="job in recentJobs"
            :key="job.id"
            dense
            :clickable="!!job.completedEntityId"
            :title="job.name"
            :subtitle="job.steps[job.currentStep]"
            @click="getVersionApiStore.handleLoad(job.completedEntityId || '')"
          >
            <template #icon>
              <q-circular-progress
                v-if="job.status === JobStatus.IN_PROGRESS"
                color="secondary"
                :value="job.currentProgress"
                size="sm"
              />
              <icon
                v-else-if="job.status === JobStatus.COMPLETED"
                variant="job-complete"
                color="primary"
              />
              <icon
                v-else-if="job.status === JobStatus.FAILED"
                variant="job-fail"
                color="error"
              />
            </template>
          </list-item>
        </list>

        <div v-if="notifications.length === 0" class="q-pa-md">
          <typography
            value="There are no notifications in the current session."
          />
        </div>
        <list v-else class="nav-notifications q-pa-sm">
          <typography variant="caption" value="Notifications" />

          <list-item
            v-for="item in notifications"
            :key="item.message"
            dense
            :title="item.message"
          >
            <template #icon>
              <icon
                v-if="item.type === MessageType.success"
                variant="save"
                color="added"
              />
              <icon
                v-if="item.type === MessageType.error"
                variant="error"
                color="removed"
              />
              <icon
                v-if="item.type === MessageType.warning"
                variant="warning"
                color="warning"
              />
              <icon
                v-if="item.type === MessageType.info"
                variant="logs"
                color="modified"
              />
            </template>
          </list-item>
        </list>
      </q-menu>
    </q-btn>
  </div>
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
import { JobStatus, MessageType } from "@/types";
import { getVersionApiStore, jobStore, logStore } from "@/hooks";
import { Typography, Icon, List, ListItem } from "@/components/common";

const viewedMessages = ref(0);

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
function handleClearNewMessages() {
  viewedMessages.value = notifications.value.length;
}
</script>
