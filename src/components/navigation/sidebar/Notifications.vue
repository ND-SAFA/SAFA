<template>
  <div>
    <q-btn round flat color="primary" @click="handleOpen">
      <icon variant="notification" />
      <q-tooltip delay="200">View notifications</q-tooltip>
      <q-badge v-if="newNotifications > 0" color="secondary" floating rounded>
        {{ newNotifications }}
      </q-badge>
      <q-menu>
        <div v-if="notifications.length === 0" class="q-pa-md">
          <typography
            value="There are no notifications in the current session."
          />
        </div>
        <q-list v-else class="nav-notifications q-pa-md">
          <q-item
            v-for="(item, index) in notifications"
            :key="index"
            dense
            class="q-px-none"
          >
            <q-item-section>
              <alert :type="item.type">
                <typography :value="item.message" />
              </alert>
            </q-item-section>
          </q-item>
        </q-list>
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
import { logStore } from "@/hooks";
import { Typography, Icon, Alert } from "@/components/common";

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
