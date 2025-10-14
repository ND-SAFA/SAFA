<template>
  <flex-box v-if="ENABLED_FEATURES.ACTIVE_USERS" l="2">
    <icon-button
      v-if="!connected"
      class="q-ml-md"
      color="negative"
      icon="disconnected"
      tooltip="Disconnected. Click to reconnect."
      @click="stompApiStore.reconnect"
    />
    <div>
      <q-avatar
        v-for="member of otherMembers"
        :key="member.tooltip"
        :color="member.color"
        size="32px"
        style="margin-right: -6px"
      >
        <typography :value="member.firstLetter" variant="subtitle" />
        <q-tooltip self="center middle">
          {{ member.tooltip }}
        </q-tooltip>
      </q-avatar>
    </div>
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays members viewing the current project.
 */
export default {
  name: "MembersBar",
};
</script>

<script lang="ts" setup>
import { computed } from "vue";
import { ENABLED_FEATURES } from "@/util";
import {
  membersStore,
  projectStore,
  sessionStore,
  stompApiStore,
} from "@/hooks";
import { FlexBox, IconButton, Typography } from "@/components/common";

const connected = computed(
  () => stompApiStore.isConnected || !projectStore.isProjectDefined
);

const members = computed(() => membersStore.activeMembers);

const otherMembers = computed(() =>
  members.value
    .filter((m) => m.email !== sessionStore.userEmail)
    .map(({ email }, idx) => {
      return {
        tooltip: `${email} currently active`,
        firstLetter: email[0].toUpperCase(),
        color: `nodeGradient${(idx % 5) + 1}`,
      };
    })
);
</script>
