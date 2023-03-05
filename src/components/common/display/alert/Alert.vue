<template>
  <q-card
    flat
    bordered
    :class="className"
    style="border-left-width: 4px !important"
  >
    <typography v-if="!!props.message" :value="props.message" />
    <slot />
  </q-card>
</template>

<script lang="ts">
/**
 * Displays a generic alert.
 */
export default {
  name: "Alert",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { MessageType } from "@/types";
import Typography from "../Typography.vue";

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
    case MessageType.ERROR:
      return "bd-negative q-pa-sm";
    case MessageType.SUCCESS:
      return "bd-positive q-pa-sm";
    case MessageType.WARNING:
      return "bd-secondary q-pa-sm";
    default:
      return "bd-primary q-pa-sm";
  }
});
</script>
