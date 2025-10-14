<template>
  <q-card flat bordered :class="className">
    <typography v-if="!!props.message" :value="props.message" />
    <slot />
  </q-card>
</template>

<script lang="ts">
/**
 * Displays a generic alert.
 */
export default {
  name: "AlertCard",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { AlertProps } from "@/types";
import { Typography } from "../content";

const props = defineProps<AlertProps>();

const className = computed(() => {
  switch (props.type) {
    case "error":
      return "bd-negative q-pa-sm nav-alert";
    case "success":
      return "bd-positive q-pa-sm nav-alert";
    case "warning":
      return "bd-secondary q-pa-sm nav-alert";
    default:
      return "bd-primary q-pa-sm nav-alert";
  }
});
</script>
