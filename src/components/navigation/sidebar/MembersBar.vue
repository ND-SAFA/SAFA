<template>
  <icon-button
    :color="color"
    :fab="false"
    :icon="icon"
    :large="true"
    :tooltip="message"
    @click="stompApiStore.connectStomp(true)"
  />
  <list :items="options">
    <template v-for="item in options" :key="item.title">
      <icon-button
        :fab="false"
        :large="true"
        :tooltip="item.toolTip"
        color="secondary"
        icon="account"
      />
    </template>
  </list>
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
import { IconVariant } from "@/types";
import { membersStore, sessionStore, stompApiStore } from "@/hooks";
import { List, IconButton } from "@/components/common";

const members = computed(() => membersStore.activeMembers);

const options = computed(() =>
  members.value
    .filter((m) => m.email !== sessionStore.userEmail)
    .map((m) => {
      return {
        title: "TITLE",
        iconTitle: "ICON TITLE",
        toolTip: m.email,
        color: "primary",
      };
    })
);

const connected = computed(() => stompApiStore.isConnected);
const color = computed(() => (connected.value ? "primary" : "negative"));
// TODO: icons
const icon = computed<IconVariant>(() =>
  connected.value ? "integrate" : "integrate"
);
const message = computed(() =>
  connected.value ? "Connected" : "Disconnected"
);
</script>
