<template>
  <icon-button
    :color="color"
    :fab="false"
    :icon-id="icon"
    :large="true"
    :tooltip="message"
    @click="stompApiStore.connectStomp"
  />
</template>

<script lang="ts">
export default {
  name: "ActiveMemberSymbol",
};
</script>

<script lang="ts" setup>
import { computed } from "vue";
import { stompApiStore } from "@/hooks";
import { IconButton } from "@/components/common";

const state = computed(() => {
  if (stompApiStore.isConnected) {
    if (stompApiStore.isAuthenticated) {
      return "connected-auth";
    } else {
      return "connected-unauth";
    }
  } else {
    return "no-connection";
  }
});
const color = computed(() => {
  if (state.value == "connected-auth") {
    return "primary";
  } else if (state.value == "connected-unauth") {
    return "orange";
  } else {
    return "red";
  }
});

const icon = computed(() => {
  if (state.value == "connected-auth") {
    return "mdi-check-circle-outline";
  } else if (state.value == "connected-unauth") {
    return "mdi-report-problem";
  } else {
    return "mdi-report-problem";
  }
});

const message = computed(() => {
  if (state.value == "connected-auth") {
    return "Connected and authenticated.";
  } else if (state.value == "connected-unauth") {
    return "Connected but not authenticated.";
  } else {
    return "No Connected";
  }
});
</script>
