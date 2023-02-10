<template>
  <v-menu offset-y top @input="handleOpen">
    <template #activator="{ props }">
      <v-btn
        icon
        size="small"
        variant="text"
        color="primary"
        v-bind="props"
        style="position: relative; right: 8px"
      >
        <v-badge
          overlap
          color="primary"
          :model-value="newNotifications > 0"
          :content="newNotifications"
        >
          <v-icon>mdi-bell-outline</v-icon>
        </v-badge>
      </v-btn>
    </template>
    <div class="neutral-bg pa-2">
      <typography
        v-if="notifications.length === 0"
        secondary
        value="There are no notifications in the current session."
      />
      <v-list v-else class="nav-notifications">
        <v-list-item v-for="(item, index) in notifications" :key="index">
          <v-alert dense outlined :type="item.type" class="full-width my-1">
            <typography :value="item.message" />
          </v-alert>
        </v-list-item>
      </v-list>
    </div>
  </v-menu>
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
import { logStore } from "@/hooks";
import { Typography } from "@/components/common";

const viewedMessages = ref(0);

const notifications = computed(() => logStore.notifications);
const newNotifications = computed(() =>
  Math.max(notifications.value.length - viewedMessages.value, 0)
);

/**
 * Sets all messages to viewed on open.
 */
function handleOpen() {
  viewedMessages.value = notifications.value.length;
}
</script>
