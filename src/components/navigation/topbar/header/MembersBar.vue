<template>
  <flex-box l="2">
    <icon-button
      v-if="!connected"
      class="q-ml-md"
      color="negative"
      icon="disconnected"
      tooltip="Disconnected. Click to reconnect."
      @click="stompApiStore.connectStomp(true)"
    />
    <div>
      <q-avatar
        v-for="member of otherMembers"
        :key="member.tooltip"
        size="32px"
        style="margin-right: -6px"
        :color="member.color"
      >
        <typography variant="subtitle" :value="member.firstLetter" />
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
