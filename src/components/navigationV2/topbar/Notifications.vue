<template>
  <v-menu offset-y @input="handleOpen">
    <template v-slot:activator="{ on, attrs }">
      <v-btn icon large color="accent" v-bind="attrs" v-on="on" class="mx-2">
        <v-badge overlap color="secondary" :value="newNotifications > 0">
          <template v-slot:badge>
            <typography
              color="primary"
              :value="newNotifications"
              style="line-height: unset; font-size: 12px !important"
            />
          </template>
          <v-icon>mdi-bell-outline</v-icon>
        </v-badge>
      </v-btn>
    </template>
    <div class="white pa-2">
      <typography
        v-if="notifications.length === 0"
        secondary
        value="There are no notifications in the current session."
      />
      <v-list v-else style="min-width: 300px">
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
import Vue from "vue";
import { SnackbarMessage } from "@/types";
import { logStore } from "@/hooks";
import { Typography } from "@/components/common";

/**
 * Displays the user's notifications.
 */
export default Vue.extend({
  name: "Notifications",
  components: { Typography },
  data() {
    return { viewedMessages: 0 };
  },
  computed: {
    /**
     * @return The current list of notifications.
     */
    notifications(): SnackbarMessage[] {
      return logStore.notifications;
    },
    /**
     * @return The number of new notifications.
     */
    newNotifications(): number {
      return Math.max(this.notifications.length - this.viewedMessages, 0);
    },
  },
  methods: {
    /**
     * Sets all messages to viewed on open.
     */
    handleOpen() {
      this.viewedMessages = this.notifications.length;
    },
  },
});
</script>
