<template>
  <q-card flat bordered :class="className">
    <slot />
  </q-card>
</template>

<script lang="ts">
/**
 * Alert
 */
export default {
  name: "Alert",
};
</script>

<script setup lang="ts">
import { computed, defineProps } from "vue";
import { MessageType } from "@/types";

const props = defineProps<{
  type: MessageType;
}>();

const className = computed(() => {
  switch (props.type) {
    case MessageType.ERROR:
      return "bd-negative q-pa-sm";
    case MessageType.SUCCESS:
      return "bd-positive q-pa-sm";
    case MessageType.WARNING:
      return "bd-warning q-pa-sm";
    default:
      return "bd-primary q-pa-sm";
  }
});
</script>
