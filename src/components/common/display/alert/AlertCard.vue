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
import { MessageType } from "@/types";
import { Typography } from "../content";

const props = defineProps<{
  /**
   * The type of alert to render.
   */
  type?: MessageType;
  /**
   * The message to render.
   */
  message?: string;
}>();

const className = computed(() => {
  switch (props.type) {
    case MessageType.error:
      return "bd-negative q-pa-sm nav-alert";
    case MessageType.success:
      return "bd-positive q-pa-sm nav-alert";
    case MessageType.warning:
      return "bd-secondary q-pa-sm nav-alert";
    default:
      return "bd-primary q-pa-sm nav-alert";
  }
});
</script>
