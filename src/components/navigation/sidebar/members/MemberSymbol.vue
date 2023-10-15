<template>
  <icon-button
    :color="color"
    :fab="false"
    :icon-id="icon"
    :large="true"
    :tooltip="message"
    @click="attemptReconnect"
  />
</template>

<script lang="ts">
export default {
  name: "MemberSymbol",
};
</script>

<script lang="ts" setup>
import { computed } from "vue";
import { stompApiStore } from "@/hooks";
import { IconButton } from "@/components/common";

const CONNECTED_AUTH = "CONNECTED_AUTH";
const CONNECTED_UNAUTH = "CONNECTED_UNAUTH";
const UNCONNECTED = "UNCONNECTED";

const colorMap = {
  CONNECTED_AUTH: "primary",
  UNCONNECTED: "red",
};

const iconMap = {
  CONNECTED_AUTH: "mdi-check-circle-outline",
  UNCONNECTED: "mdi-close-octagon",
};

const messageMap: Record<string, string> = {
  CONNECTED_AUTH: "Connected.",
  UNCONNECTED: "No Connected",
};

const state = computed(() => {
  return stompApiStore.isConnected ? CONNECTED_AUTH : UNCONNECTED;
});
const color = computed(() => {
  return colorMap[state.value];
});

const icon = computed(() => {
  return iconMap[state.value];
});

const message = computed(() => {
  return messageMap[state.value];
});

function attemptReconnect() {
  stompApiStore.connectStomp(true);
}
</script>
